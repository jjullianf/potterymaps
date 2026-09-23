// Gemeinsame Daten fuer alle Blog-Artikel unter site/ch/blog/ - jeder Artikel
// liefert nur noch Inhalt + Metadaten (headline, teaser, datePublished, faqs, ...),
// Layout, Permalink, Collection-Zugehoerigkeit und alle Schema.org-Markups
// (Article, FAQPage, BreadcrumbList) werden hier einheitlich erzeugt.
module.exports = {
  layout: "blog-post.njk",
  tags: "blog",
  permalink: (data) => `/ch/blog/${data.page.fileSlug}/`,
  eleventyComputed: {
    jsonLd: (data) => ({
      "@context": "https://schema.org",
      "@type": "Article",
      headline: data.headline,
      description: data.teaser,
      author: { "@type": "Organization", name: "potterymaps" },
      publisher: {
        "@type": "Organization",
        name: "potterymaps",
        logo: { "@type": "ImageObject", url: `${data.site.url}/images/logo.png` },
      },
      datePublished: data.datePublished,
      dateModified: data.dateModified || data.datePublished,
      mainEntityOfPage: `${data.site.url}/ch/blog/${data.page.fileSlug}/`,
      image: data.ogImage || `${data.site.url}/images/hero-keramik.jpg`,
    }),
    jsonLdFaq: (data) =>
      data.faqs && data.faqs.length
        ? {
            "@context": "https://schema.org",
            "@type": "FAQPage",
            mainEntity: data.faqs.map((f) => ({
              "@type": "Question",
              name: f.q,
              acceptedAnswer: { "@type": "Answer", text: f.a },
            })),
          }
        : null,
    jsonLdBreadcrumb: (data) => ({
      "@context": "https://schema.org",
      "@type": "BreadcrumbList",
      itemListElement: [
        { "@type": "ListItem", position: 1, name: "Startseite", item: `${data.site.url}/ch/` },
        { "@type": "ListItem", position: 2, name: "Blog", item: `${data.site.url}/ch/blog/` },
        { "@type": "ListItem", position: 3, name: data.headline, item: `${data.site.url}/ch/blog/${data.page.fileSlug}/` },
      ],
    }),
  },
};
