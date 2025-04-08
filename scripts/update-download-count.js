const axios = require('axios');
const fs = require('fs');

const OWNER = 'Hayato-shino05';
const REPO = 'tool-tim-kiem-thanh-le-hom-nay';

const getDownloadCounts = async () => {
  const res = await axios.get(`https://api.github.com/repos/${OWNER}/${REPO}/releases`);
  const releases = res.data;

  let apkCount = 0;
  let exeCount = 0;

  for (const release of releases) {
    for (const asset of release.assets) {
      if (asset.name.endsWith('.apk')) apkCount += asset.download_count;
      if (asset.name.endsWith('.exe')) exeCount += asset.download_count;
    }
  }

  return { apkCount, exeCount, total: apkCount + exeCount };
};

const updateReadme = async () => {
  const { apkCount, exeCount, total } = await getDownloadCounts();
  const badge = `
<p align="center">
  <img src="https://img.shields.io/badge/Tổng_lượt_tải-${total}-brightgreen?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Android-${apkCount}-orange?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Windows-${exeCount}-blue?style=for-the-badge" />
</p>
`;

  let readme = fs.readFileSync('README.md', 'utf8');
  readme = readme.replace(
    /<p align="center">[\s\S]*?<\/p>/,
    badge.trim()
  );

  fs.writeFileSync('README.md', readme, 'utf8');
};

updateReadme();
