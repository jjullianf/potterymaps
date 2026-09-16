// Lokaler Server fuer den Keramik-Verzeichnis Editor.
// Speichert Aenderungen direkt in data/studios.json (statt im Browser),
// legt bei jedem Speichern ein Backup der vorherigen Version an und
// speichert hochgeladene Fotos als echte Dateien statt Base64-Text.

const express = require('express');
const multer = require('multer');
const fs = require('fs');
const path = require('path');

const PORT = process.env.PORT || 4000;
const ROOT = __dirname;
const DATA_DIR = path.join(ROOT, 'data');
const BACKUP_DIR = path.join(DATA_DIR, 'backups');
const STATE_FILE = path.join(DATA_DIR, 'studios.json');
const FOTOS_DIR = path.join(ROOT, 'fotos');
const IMPORT_CSV = path.join(ROOT, '..', 'keramik-bemalen-schweiz-FINAL-fuer-editor-import.csv');
const MAX_BACKUPS = 200; // alte Backups werden darueber hinaus abgeraeumt, damit der Ordner nicht unbegrenzt waechst

for (const dir of [DATA_DIR, BACKUP_DIR, FOTOS_DIR]) {
  fs.mkdirSync(dir, { recursive: true });
}

// ---------- CSV Parsing (nur fuer den einmaligen Erst-Import) ----------

function parseCSV(text) {
  const rows = [];
  let row = [], field = '', inQuotes = false;
  for (let i = 0; i < text.length; i++) {
    const c = text[i], next = text[i + 1];
    if (inQuotes) {
      if (c === '"' && next === '"') { field += '"'; i++; }
      else if (c === '"') { inQuotes = false; }
      else { field += c; }
    } else {
      if (c === '"') inQuotes = true;
      else if (c === ',') { row.push(field); field = ''; }
      else if (c === '\r') { /* skip */ }
      else if (c === '\n') { row.push(field); rows.push(row); row = []; field = ''; }
      else field += c;
    }
  }
  if (field.length || row.length) { row.push(field); rows.push(row); }
  return rows.filter(r => r.length > 1 || r[0] !== '');
}

function loadFromCSV(csvPath) {
  let text = fs.readFileSync(csvPath, 'utf8');
  if (text.charCodeAt(0) === 0xFEFF) text = text.slice(1);
  const rows = parseCSV(text);
  const header = rows[0];
  const studios = [];
  const reviewed = {};
  for (let i = 1; i < rows.length; i++) {
    const obj = {};
    header.forEach((h, idx) => { obj[h] = rows[i][idx] || ''; });
    if (obj.slug) {
      reviewed[obj.slug] = obj.reviewed === 'true';
      delete obj.reviewed;
      studios.push(obj);
    }
  }
  return { studios, reviewed };
}

// ---------- Zustand laden / initialisieren ----------
// WICHTIG: studios.json wird NUR aus der CSV importiert, wenn sie noch nicht
// existiert. Existiert sie bereits, wird sie unter keinen Umstaenden ueberschrieben.

function ensureInitialState() {
  if (fs.existsSync(STATE_FILE)) {
    console.log(`studios.json existiert bereits - CSV-Import wird uebersprungen (${STATE_FILE})`);
    return;
  }
  if (!fs.existsSync(IMPORT_CSV)) {
    console.log('Keine studios.json und kein Import-CSV gefunden - starte mit leerem Datenbestand.');
    fs.writeFileSync(STATE_FILE, JSON.stringify({ studios: [], reviewed: {} }, null, 2), 'utf8');
    return;
  }
  console.log(`Erst-Import aus ${path.basename(IMPORT_CSV)} ...`);
  const state = loadFromCSV(IMPORT_CSV);
  fs.writeFileSync(STATE_FILE, JSON.stringify(state, null, 2), 'utf8');
  console.log(`${state.studios.length} Studios importiert -> ${STATE_FILE}`);
}

ensureInitialState();

// ---------- Backup-Verwaltung ----------

function timestamp() {
  const d = new Date();
  const pad = (n) => String(n).padStart(2, '0');
  return `${d.getFullYear()}${pad(d.getMonth() + 1)}${pad(d.getDate())}-${pad(d.getHours())}${pad(d.getMinutes())}${pad(d.getSeconds())}-${String(d.getMilliseconds()).padStart(3, '0')}`;
}

function backupCurrentState() {
  if (!fs.existsSync(STATE_FILE)) return;
  const dest = path.join(BACKUP_DIR, `studios-${timestamp()}.json`);
  fs.copyFileSync(STATE_FILE, dest);
  pruneOldBackups();
}

function pruneOldBackups() {
  const files = fs.readdirSync(BACKUP_DIR)
    .filter(f => f.endsWith('.json'))
    .map(f => ({ f, t: fs.statSync(path.join(BACKUP_DIR, f)).mtimeMs }))
    .sort((a, b) => b.t - a.t);
  for (const { f } of files.slice(MAX_BACKUPS)) {
    fs.unlinkSync(path.join(BACKUP_DIR, f));
  }
}

// ---------- Hilfsfunktionen ----------

function safeSlug(slug) {
  return typeof slug === 'string' && /^[a-z0-9-]+$/.test(slug) ? slug : null;
}

function slugPhotoDir(slug) {
  return path.join(FOTOS_DIR, slug);
}

// ---------- App ----------

const app = express();
app.use(express.json({ limit: '5mb' }));
app.use(express.static(path.join(ROOT, 'public')));
app.use('/fotos', express.static(FOTOS_DIR));

// Aktuellen Zustand laden
app.get('/api/state', (req, res) => {
  try {
    const raw = fs.readFileSync(STATE_FILE, 'utf8');
    res.type('application/json').send(raw);
  } catch (e) {
    res.status(500).json({ error: 'Konnte studios.json nicht lesen.', detail: String(e) });
  }
});

// Zustand speichern (mit automatischem Backup der vorherigen Version)
app.put('/api/state', (req, res) => {
  const body = req.body;
  if (!body || !Array.isArray(body.studios)) {
    return res.status(400).json({ error: 'Erwarte { studios: [...], reviewed: {...} }' });
  }
  try {
    backupCurrentState();
    fs.writeFileSync(STATE_FILE, JSON.stringify({ studios: body.studios, reviewed: body.reviewed || {} }, null, 2), 'utf8');
    res.json({ ok: true, savedAt: new Date().toISOString() });
  } catch (e) {
    res.status(500).json({ error: 'Speichern fehlgeschlagen.', detail: String(e) });
  }
});

// Fotos eines Studios auflisten
app.get('/api/photos/:slug', (req, res) => {
  const slug = safeSlug(req.params.slug);
  if (!slug) return res.status(400).json({ error: 'Ungueltiger slug' });
  const dir = slugPhotoDir(slug);
  if (!fs.existsSync(dir)) return res.json([]);
  const files = fs.readdirSync(dir)
    .filter(f => /\.(jpe?g|png|webp|gif)$/i.test(f))
    .map(f => ({ f, t: fs.statSync(path.join(dir, f)).mtimeMs }))
    .sort((a, b) => a.t - b.t)
    .map(({ f }) => ({ name: f, url: `/fotos/${encodeURIComponent(slug)}/${encodeURIComponent(f)}` }));
  res.json(files);
});

// Fotos hochladen (mehrere moeglich), landen als echte Dateien in fotos/[slug]/
const upload = multer({
  storage: multer.diskStorage({
    destination: (req, file, cb) => {
      const slug = safeSlug(req.params.slug);
      if (!slug) return cb(new Error('Ungueltiger slug'));
      const dir = slugPhotoDir(slug);
      fs.mkdirSync(dir, { recursive: true });
      cb(null, dir);
    },
    filename: (req, file, cb) => {
      const base = path.basename(file.originalname, path.extname(file.originalname))
        .replace(/[^a-zA-Z0-9_-]+/g, '-')
        .slice(0, 60) || 'foto';
      const ext = /\.(jpe?g|png|webp|gif)$/i.test(file.originalname) ? path.extname(file.originalname) : '.jpg';
      cb(null, `${Date.now()}-${base}${ext}`);
    },
  }),
  limits: { fileSize: 15 * 1024 * 1024, files: 20 },
  fileFilter: (req, file, cb) => {
    cb(null, /^image\//.test(file.mimetype));
  },
});

app.post('/api/photos/:slug', upload.array('photos', 20), (req, res) => {
  const slug = safeSlug(req.params.slug);
  if (!slug) return res.status(400).json({ error: 'Ungueltiger slug' });
  const files = (req.files || []).map(f => ({
    name: f.filename,
    url: `/fotos/${encodeURIComponent(slug)}/${encodeURIComponent(f.filename)}`,
  }));
  res.json(files);
});

// Einzelnes Foto loeschen
app.delete('/api/photos/:slug/:filename', (req, res) => {
  const slug = safeSlug(req.params.slug);
  if (!slug) return res.status(400).json({ error: 'Ungueltiger slug' });
  const filename = path.basename(req.params.filename); // schuetzt vor Path-Traversal
  const filePath = path.join(slugPhotoDir(slug), filename);
  if (fs.existsSync(filePath)) fs.unlinkSync(filePath);
  res.json({ ok: true });
});

app.listen(PORT, () => {
  console.log(`\nKeramik-Verzeichnis Editor laeuft auf http://localhost:${PORT}\n`);
});
