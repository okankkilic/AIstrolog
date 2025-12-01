interface DailyRanking {
  burc: string;
  score: number;
}

interface CategoryRankings {
  genel_ranking: DailyRanking[];
  aşk_ranking: DailyRanking[];
  para_ranking: DailyRanking[];
  sağlık_ranking: DailyRanking[];
}

interface RankingsHistory {
  [date: string]: CategoryRankings;
}

interface SignRanking {
  sign: string;
  slug: string;
  score: number;
}

interface RankingsData {
  general: SignRanking[];
  love: SignRanking[];
  money: SignRanking[];
  health: SignRanking[];
}

// Convert Turkish sign names to slugs
const signToSlug: Record<string, string> = {
  'Koç': 'koc',
  'Boğa': 'boga',
  'İkizler': 'ikizler',
  'Yengeç': 'yengec',
  'Aslan': 'aslan',
  'Başak': 'basak',
  'Terazi': 'terazi',
  'Akrep': 'akrep',
  'Yay': 'yay',
  'Oğlak': 'oglak',
  'Kova': 'kova',
  'Balık': 'balik'
};

/**
 * Calculate rankings from rankings_history.json
 * @param period - 'daily', 'weekly', or 'monthly'
 * @param historyData - The rankings history JSON data
 * @returns Calculated rankings
 */
export function calculateRankings(
  period: 'daily' | 'weekly' | 'monthly',
  historyData: RankingsHistory
): RankingsData | null {
  const dates = Object.keys(historyData)
    .sort((a, b) => new Date(b).getTime() - new Date(a).getTime()); // Most recent first (chronological)
  
  if (dates.length === 0) {
    return null;
  }

  // Determine how many days to include
  let daysToInclude: number;
  switch (period) {
    case 'daily':
      daysToInclude = 1;
      break;
    case 'weekly':
      daysToInclude = 7;
      break;
    case 'monthly':
      daysToInclude = 30;
      break;
  }

  // Get the relevant dates
  const relevantDates = dates.slice(0, daysToInclude);
  
  if (relevantDates.length === 0) {
    return null;
  }

  // Calculate average scores for each sign and category
  const signScores: Record<string, {
    general: number[];
    love: number[];
    money: number[];
    health: number[];
  }> = {};

  // Initialize all signs
  Object.keys(signToSlug).forEach(sign => {
    signScores[sign] = { general: [], love: [], money: [], health: [] };
  });

  // Collect scores from relevant dates
  relevantDates.forEach(date => {
    const dayData = historyData[date];
    
    // General rankings
    dayData.genel_ranking?.forEach(item => {
      if (signScores[item.burc]) {
        signScores[item.burc].general.push(item.score);
      }
    });

    // Love rankings
    dayData.aşk_ranking?.forEach(item => {
      if (signScores[item.burc]) {
        signScores[item.burc].love.push(item.score);
      }
    });

    // Money rankings
    dayData.para_ranking?.forEach(item => {
      if (signScores[item.burc]) {
        signScores[item.burc].money.push(item.score);
      }
    });

    // Health rankings
    dayData.sağlık_ranking?.forEach(item => {
      if (signScores[item.burc]) {
        signScores[item.burc].health.push(item.score);
      }
    });
  });

  // Calculate averages and create rankings
  const calculateAverage = (scores: number[]) => {
    if (scores.length === 0) return 0;
    return scores.reduce((a, b) => a + b, 0) / scores.length;
  };

  const createRanking = (category: 'general' | 'love' | 'money' | 'health'): SignRanking[] => {
    const rankings = Object.entries(signScores).map(([sign, scores]) => ({
      sign,
      slug: signToSlug[sign],
      score: Math.round(calculateAverage(scores[category]) * 10) / 10
    }));

    // Sort by score descending
    return rankings.sort((a, b) => b.score - a.score);
  };

  return {
    general: createRanking('general'),
    love: createRanking('love'),
    money: createRanking('money'),
    health: createRanking('health')
  };
}

/**
 * Fetch rankings - tries backend first, falls back to client-side calculation
 */
export async function fetchRankings(
  period: 'daily' | 'weekly' | 'monthly',
  backendUrl?: string
): Promise<RankingsData | null> {
  // First, try to load from /data/rankings_history.json and calculate locally
  try {
    const response = await fetch('/data/rankings_history.json');
    if (response.ok) {
      const historyData: RankingsHistory = await response.json();
      return calculateRankings(period, historyData);
    }
    // If file not found or not ok, fall through to API
  } catch (error) {
    // If fetch fails (e.g. file not found), try API
  }

  // Fallback: Try backend API if URL provided
  if (backendUrl) {
    try {
      const getTodayDate = () => {
        const today = new Date();
        return `${String(today.getDate()).padStart(2, '0')}-${String(today.getMonth() + 1).padStart(2, '0')}-${today.getFullYear()}`;
      };
      const response = await fetch(`${backendUrl}/api/rankings/${getTodayDate()}?period=${period}`, {
        signal: AbortSignal.timeout(3000) // 3 second timeout
      });
      if (response.ok) {
        const data = await response.json();
        return data.rankings;
      }
    } catch (error) {
      console.log('Backend unavailable, no rankings data found');
    }
  }
  // If neither source works, return null
  return null;
}
