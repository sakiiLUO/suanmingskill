/**
 * 紫微斗数桥接：把 Python 传来的出生信息交给 iztro（MIT）排盘，输出 JSON。
 *
 * 为什么用桥接而不是移植：iztro 是维护活跃、许可证明确的成熟实现（十二宫/主星/辅星/
 * 四化/大限/流年），移植成本高且易错；这里只做数据搬运，不复制其代码。
 *
 * 用法（由 scripts/ziwei.py 调用）：
 *   node scripts/ziwei_bridge.cjs '{"date":"1995-8-17","timeIndex":7,"gender":"male","year":2026}'
 */
const path = require('path');

function loadIztro() {
  const candidates = [
    path.join(__dirname, '..', 'vendor', 'iztro', 'node_modules', 'iztro'),
    'iztro',
  ];
  let lastError = null;
  for (const candidate of candidates) {
    try {
      return require(candidate);
    } catch (error) {
      lastError = error;
    }
  }
  throw lastError || new Error('iztro not found');
}

function star(star) {
  return {
    name: star.name,
    type: star.type,
    brightness: star.brightness || '',
    mutagen: star.mutagen || '',
  };
}

function main() {
  const input = JSON.parse(process.argv[2] || '{}');
  const { astro } = loadIztro();
  const gender = input.gender === 'female' ? '女' : '男';
  const astrolabe = astro.bySolar(
    input.date,
    Number(input.timeIndex),
    gender,
    input.fixLeap !== false,
    input.language || 'zh-CN',
  );

  const palaces = astrolabe.palaces.map((palace) => ({
    name: palace.name,
    heavenlyStem: palace.heavenlyStem,
    earthlyBranch: palace.earthlyBranch,
    isBodyPalace: Boolean(palace.isBodyPalace),
    isOriginalPalace: Boolean(palace.isOriginalPalace),
    majorStars: (palace.majorStars || []).map(star),
    minorStars: (palace.minorStars || []).map(star),
    adjectiveStars: (palace.adjectiveStars || []).map((s) => s.name),
    changsheng12: palace.changsheng12,
    decadal: palace.decadal
      ? {
          range: palace.decadal.range,
          heavenlyStem: palace.decadal.heavenlyStem,
          earthlyBranch: palace.decadal.earthlyBranch,
        }
      : null,
  }));

  const out = {
    solarDate: astrolabe.solarDate,
    lunarDate: astrolabe.lunarDate,
    chineseDate: astrolabe.chineseDate,
    time: astrolabe.time,
    timeRange: astrolabe.timeRange,
    fiveElementsClass: astrolabe.fiveElementsClass,
    soul: astrolabe.soul,
    body: astrolabe.body,
    earthlyBranchOfSoulPalace: astrolabe.earthlyBranchOfSoulPalace,
    earthlyBranchOfBodyPalace: astrolabe.earthlyBranchOfBodyPalace,
    zodiac: astrolabe.zodiac,
    sign: astrolabe.sign,
    palaces,
    copyright: 'iztro (MIT) https://github.com/SylarLong/iztro',
  };

  if (input.year) {
    try {
      const horoscope = astrolabe.horoscope(`${input.year}-06-01`);
      out.horoscope = {
        year: input.year,
        decadal: horoscope.decadal
          ? {
              heavenlyStem: horoscope.decadal.heavenlyStem,
              earthlyBranch: horoscope.decadal.earthlyBranch,
              palaceNames: horoscope.decadal.palaceNames,
              mutagen: horoscope.decadal.mutagen,
            }
          : null,
        yearly: horoscope.yearly
          ? {
              heavenlyStem: horoscope.yearly.heavenlyStem,
              earthlyBranch: horoscope.yearly.earthlyBranch,
              palaceNames: horoscope.yearly.palaceNames,
              mutagen: horoscope.yearly.mutagen,
            }
          : null,
      };
    } catch (error) {
      out.horoscopeError = String(error && error.message ? error.message : error);
    }
  }

  process.stdout.write(JSON.stringify(out));
}

main();
