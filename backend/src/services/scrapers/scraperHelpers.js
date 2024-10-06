// Helper functions in scrapers
export const getTextContent = (selector) => {
  // Simplifies text extraction and handle cases where element might not exist
  const element = document.querySelector(selector);
  return element ? element.textContent.trim() : 'N/A';
};

export const getAllProductImages = () => {
  const imageLinks = document.querySelectorAll('#imgs a.itm');
  return Array.from(imageLinks).map(link => {
    const img = link.querySelector('img');
    return {
      largeImageUrl: link.href,
      thumbnailUrl: img.dataset.src || img.src,
      alt: img.alt
    };
  });
};

export const getSpecification = () => {
  const specs = {};

  // Get specifications from the first section
  const specElement = document.querySelector('.markup.-mhm.-pvl.-oxa.-sc');
  if (specElement) {
    let currentCategory = '';
    Array.from(specElement.children).forEach(child => {
      if (child.tagName === 'P') {
        currentCategory = child.textContent.trim();
        specs[currentCategory] = {};
      } else if (child.tagName === 'UL') {
        const items = Array.from(child.querySelectorAll('li'));
        items.forEach(item => {
          const [key, value] = item.textContent.split(':').map(s => s.trim());
          if (key && value) {
            specs[currentCategory][key] = value;
          } else {
            // Handle cases where there's no colon separator
            specs[currentCategory][item.textContent.trim()] = true;
          }
        });
      }
    });
  }

  // Get specifications from the second section
  const secondSpecSection = document.querySelector('section.card.aim.-mtm.-fs16');
  if (secondSpecSection) {
    const articles = secondSpecSection.querySelectorAll('article');
    articles.forEach(article => {
      const title = article.querySelector('h2').textContent.trim();
      specs[title] = {};

      const listItems = article.querySelectorAll('ul li, ul.-pvs.-mvxs.-phm.-lsn li');
      listItems.forEach(item => {
        const key = item.querySelector('span.-b');
        if (key) {
          const keyText = key.textContent.trim();
          const valueText = item.textContent.replace(keyText, '').trim().replace(':', '').trim();
          specs[title][keyText] = valueText;
        } else {
          specs[title][item.textContent.trim()] = true;
        }
      });
    });
  }
  return specs;
};

export const scraperHelpersString = `
${getTextContent.toString()}
${getAllProductImages.toString()}
${getSpecification.toString()}
`;
