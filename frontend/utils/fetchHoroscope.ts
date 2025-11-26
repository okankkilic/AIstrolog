interface HoroscopeData {
  general: string;
  love: string;
  money: string;
  health: string;
}

interface DailySummaryData {
  [signName: string]: {
    genel: string;
    aşk: string;
    para: string;
    sağlık: string;
  };
}

// Map Turkish sign names to slugs
const SIGN_NAME_MAP: Record<string, string> = {
  'koc': 'Koç',
  'boga': 'Boğa',
  'ikizler': 'İkizler',
  'yengec': 'Yengeç',
  'aslan': 'Aslan',
  'basak': 'Başak',
  'terazi': 'Terazi',
  'akrep': 'Akrep',
  'yay': 'Yay',
  'oglak': 'Oğlak',
  'kova': 'Kova',
  'balik': 'Balık'
};

/**
 * Convert DD-MM-YYYY to YYYY-MM-DD format for JSON file lookup
 */
function convertDateFormat(dateStr: string): string {
  const parts = dateStr.split('-');
  if (parts.length === 3) {
    const [day, month, year] = parts;
    return `${year}-${month}-${day}`;
  }
  return dateStr;
}

/**
 * Fetch horoscope data - tries backend first, falls back to JSON
 */
export async function fetchHoroscope(
  signSlug: string,
  date: string,
  backendUrl?: string
): Promise<HoroscopeData | null> {
  const signName = SIGN_NAME_MAP[signSlug];
  
  if (!signName) {
    console.error(`Unknown sign slug: ${signSlug}`);
    return null;
  }

  // First, try to load from JSON summary file
  try {
    const jsonDate = convertDateFormat(date);
    const response = await fetch(`/data/summarized_processed_daily_raw_${jsonDate}.json`);
    if (response.ok) {
      const data: DailySummaryData = await response.json();
      const signData = data[signName];
      if (signData) {
        // Map Turkish keys to English
        return {
          general: signData.genel || '',
          love: signData.aşk || '',
          money: signData.para || '',
          health: signData.sağlık || ''
        };
      }
    }
    // If file not found or sign not found, fall through to API
  } catch (error) {
    // If fetch fails (e.g. file not found), try API
  }

  // Fallback: Try backend API if URL provided
  if (backendUrl) {
    try {
      const response = await fetch(`${backendUrl}/api/gunluk/${signSlug}/${date}`, {
        signal: AbortSignal.timeout(3000) // 3 second timeout
      });
      if (response.ok) {
        const data = await response.json();
        return data.horoscope;
      }
    } catch (error) {
      console.log('Backend unavailable, no horoscope data found');
    }
  }
  // If neither source works, return null
  return null;
}

/**
 * Try to find horoscope data going back up to maxDays
 */
export async function fetchHoroscopeWithFallback(
  signSlug: string,
  date: string,
  maxDays: number = 7,
  backendUrl?: string
): Promise<{ data: HoroscopeData; actualDate: string } | null> {
  const parseDateAndGoBack = (dateStr: string, daysBack: number): string => {
    const parts = dateStr.split('-');
    if (parts.length === 3) {
      const day = parseInt(parts[0]);
      const month = parseInt(parts[1]) - 1; // JS months are 0-indexed
      const year = parseInt(parts[2]);
      const dateObj = new Date(year, month, day);
      dateObj.setDate(dateObj.getDate() - daysBack);
      
      const newDay = String(dateObj.getDate()).padStart(2, '0');
      const newMonth = String(dateObj.getMonth() + 1).padStart(2, '0');
      const newYear = dateObj.getFullYear();
      return `${newDay}-${newMonth}-${newYear}`;
    }
    return dateStr;
  };

  for (let daysBack = 0; daysBack < maxDays; daysBack++) {
    const targetDate = parseDateAndGoBack(date, daysBack);
    const data = await fetchHoroscope(signSlug, targetDate, backendUrl);
    
    if (data) {
      return { data, actualDate: targetDate };
    }
  }

  return null;
}
