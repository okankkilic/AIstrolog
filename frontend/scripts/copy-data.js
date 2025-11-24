const fs = require('fs');
const path = require('path');

const sourceDir = path.join(__dirname, '../../data');
const destDir = path.join(__dirname, '../public/data');

// Clean destination directory
if (fs.existsSync(destDir)) {
  fs.rmSync(destDir, { recursive: true });
}
fs.mkdirSync(destDir, { recursive: true });

// Copy rankings_history.json
const rankingsFile = 'rankings_history.json';
const rankingsSource = path.join(sourceDir, rankingsFile);
if (fs.existsSync(rankingsSource)) {
  fs.copyFileSync(rankingsSource, path.join(destDir, rankingsFile));
  console.log(`✅ Copied ${rankingsFile}`);
}

// Copy all summarized_processed_daily_raw_*.json files
const files = fs.readdirSync(sourceDir);
const summarizedFiles = files.filter(file => 
  file.startsWith('summarized_processed_daily_raw_') && file.endsWith('.json')
);

summarizedFiles.forEach(file => {
  fs.copyFileSync(
    path.join(sourceDir, file),
    path.join(destDir, file)
  );
  console.log(`✅ Copied ${file}`);
});

console.log(`\n📦 Total files copied: ${summarizedFiles.length + 1}`);
