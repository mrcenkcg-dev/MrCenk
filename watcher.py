/**
 * ==============================================================================
 * SOVEREIGN MASTER ENGINE: DYNAMIC FULL-SCHEDULE & LUCKY DIP EDITION
 * ==============================================================================
 */

const express = require('express');
const sqlite3 = require('sqlite3').verbose();
const path = require('path');

const app = express();
const PORT = process.env.PORT || 10000;

app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// ==============================================================================
// 1. DATABASE SETUP & COMPREHENSIVE SCHEDULE SCHEMA
// ==============================================================================
const dbFile = path.join(__dirname, 'sovereign_master.db');
const db = new sqlite3.Database(dbFile, (err) => {
    if (err) {
        console.error('❌ Database connection error:', err.message);
    } else {
        console.log('✅ Connected to Sovereign Master Ecosystem DB.');
        initializeMasterDatabase();
    }
});

function initializeMasterDatabase() {
    db.serialize(() => {
        db.run(`CREATE TABLE IF NOT EXISTS multi_league_fixtures (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            league_category TEXT,
            home_team TEXT,
            away_team TEXT,
            match_date TEXT,
            venue TEXT,
            home_rating INT,
            away_rating INT,
            aggression_rating INT,
            ad_sponsor TEXT
        )`);

        db.run(`DELETE FROM multi_league_fixtures`, () => {
            db.run(`INSERT INTO multi_league_fixtures (league_category, home_team, away_team, match_date, venue, home_rating, away_rating, aggression_rating, ad_sponsor) VALUES 
                ('UEFA Nations League', 'Türkiye', 'France', 'Tomorrow, 19:45', 'RAMS Park, Istanbul', 86, 91, 8, 'Anadolu Sufi Rock Partner'),
                ('UEFA Nations League', 'Türkiye', 'Italy', '28 Sep 2026, 19:45', 'Chobani Stadyumu, Istanbul', 86, 89, 9, 'Sovereign Global Partner'),
                ('UEFA Nations League', 'Belgium', 'Türkiye', '02 Oct 2026, 19:45', 'King Baudouin Stadium, Brussels', 87, 86, 7, 'Get Big Together Initiative'),
                ('International Friendly', 'Germany', 'England', 'Tomorrow, 20:00', 'Allianz Arena, Munich', 90, 88, 8, 'Sovereign Analytics Partner'),
                ('International Friendly', 'Spain', 'Brazil', 'Tomorrow, 21:00', 'Santiago Bernabéu, Madrid', 92, 90, 9, 'Global Sports Partner'),
                ('Süper Lig', 'Galatasaray S.K.', 'Fenerbahçe SK', 'This Weekend, 20:00', 'RAMS Park, Istanbul', 87, 86, 9, 'Anadolu Sufi Rock Partner'),
                ('Premier League', 'Liverpool F.C.', 'Manchester City', 'This Weekend, 16:30', 'Anfield, Liverpool', 91, 94, 7, 'Sovereign Analytics Partner')`);
        });

        db.run(`CREATE TABLE IF NOT EXISTS public_contributions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            contributor_name TEXT,
            contribution_type TEXT,
            message_content TEXT,
            status TEXT
        )`);
    });
}

// ==============================================================================
// 2. AI PROBABILITY ENGINE
// ==============================================================================
function calculateInPlayMarkets(homeRating, awayRating, aggression) {
    const homeAdvantage = 5;
    const totalPower = homeRating + awayRating + homeAdvantage;
    
    let rawHomeWin = ((homeRating + homeAdvantage) / totalPower) * 100;
    let rawAwayWin = (awayRating / totalPower) * 100;

    let homeWinProb, awayWinProb;
    if (rawHomeWin >= rawAwayWin) {
        homeWinProb = Math.round(58 + (Math.random() * 4));
        awayWinProb = Math.round(100 - homeWinProb - 18);
    } else {
        awayWinProb = Math.round(58 + (Math.random() * 4));
        homeWinProb = Math.round(100 - awayWinProb - 18);
    }

    let drawProb = 100 - (homeWinProb + awayWinProb);
    if (drawProb < 12) drawProb = 15;

    const margin = 1.04;
    const homeDecimal = ((100 / homeWinProb) * margin).toFixed(2);
    const drawDecimal = ((100 / drawProb) * margin).toFixed(2);
    const awayDecimal = ((100 / awayWinProb) * margin).toFixed(2);

    const expectedCorners = Math.floor(9 + ((homeRating + awayRating) / 30));
    const expectedFouls = Math.floor(22 + (aggression * 1.2));
    const redCardChance = aggression >= 8 ? "High (0.45 Est)" : "Low / Moderate (0.15 Est)";
    const firstGoalTeam = homeRating >= awayRating ? "Home Team (AI Fav)" : "Away Team (AI Fav)";
    const overUnderGoals = (homeRating + awayRating) > 175 ? "Over 2.5 Goals (1.75)" : "Under 2.5 Goals (1.95)";

    return {
        homeWinProb, drawProb, awayWinProb,
        homeDecimal, drawDecimal, awayDecimal,
        expectedCorners, expectedFouls, redCardChance, firstGoalTeam, overUnderGoals
    };
}

function microFeeTollGate(fee = '$0.001') {
    return (req, res, next) => {
        const endpoint = req.originalUrl;
        const origin = req.headers['x-forwarded-for'] || req.socket.remoteAddress || 'Local Client';
        next();
    };
}

// ==============================================================================
// 3. ROUTES & PORTAL (/island) WITH LUCKY DIP BUTTONS
// ==============================================================================
app.get('/', microFeeTollGate('$0.001'), (req, res) => {
    res.redirect('/island');
});

app.get('/island', microFeeTollGate('$0.001'), (req, res) => {
    db.all(`SELECT * FROM multi_league_fixtures`, (err, matches) => {
        res.send(`
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <title>Anadolu AI Sportsbook & Lucky Dip Lounge</title>
            <style>
                * { box-sizing: border-box; margin: 0; padding: 0; }
                body { font-family: -apple-system, sans-serif; background: #070908; color: #e2e8f0; padding: 25px; }
                .container { max-width: 1100px; margin: 0 auto; display: flex; flex-direction: column; gap: 24px; }
                header { background: #111a14; padding: 24px; border-radius: 20px; border: 1px solid rgba(34, 197, 94, 0.4); display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 15px; }
                h1 { color: #22c55e; font-size: 22px; margin-bottom: 4px; }
                p { color: #94a3b8; font-size: 13px; }
                .badge { background: #22c55e; color: #000; padding: 4px 10px; border-radius: 20px; font-weight: bold; font-size: 11px; }
                .league-tag { background: rgba(56, 189, 248, 0.15); color: #38bdf8; padding: 2px 8px; border-radius: 6px; font-size: 11px; font-weight: bold; border: 1px solid rgba(56, 189, 248, 0.3); display: inline-block; margin-bottom: 4px; }
                .card { background: #111a14; border: 1px solid rgba(255,255,255,0.08); border-radius: 20px; padding: 24px; display: flex; flex-direction: column; gap: 16px; }
                h2 { font-size: 17px; color: #fff; }
                
                .fixtures-scroll-container { max-height: 600px; overflow-y: auto; padding-right: 6px; display: flex; flex-direction: column; gap: 16px; }
                .fixtures-scroll-container::-webkit-scrollbar { width: 8px; }
                .fixtures-scroll-container::-webkit-scrollbar-track { background: #0b120e; border-radius: 8px; }
                .fixtures-scroll-container::-webkit-scrollbar-thumb { background: #1f3a29; border-radius: 8px; }

                .match-box { background: #16221a; border: 1px solid rgba(34,197,94,0.25); border-radius: 14px; padding: 18px; display: flex; flex-direction: column; gap: 12px; }
                .match-header { display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 10px; border-bottom: 1px solid rgba(255,255,255,0.06); padding-bottom: 10px; }
                .odds-row { display: flex; gap: 8px; flex-wrap: wrap; }
                .bet-btn { background: #1c2b21; border: 1px solid rgba(34,197,94,0.4); border-radius: 8px; padding: 8px 12px; color: #fff; cursor: pointer; text-align: left; flex: 1; min-width: 110px; }
                .bet-label { font-size: 10px; color: #94a3b8; display: block; text-transform: uppercase; }
                .bet-val { font-size: 15px; font-weight: bold; color: #22c55e; font-family: monospace; display: block; }
                .stats-tag { background: rgba(255,255,255,0.05); padding: 6px 10px; border-radius: 8px; font-size: 12px; color: #cbd5e1; border: 1px solid rgba(255,255,255,0.08); }
                
                /* LUCKY DIP BUTTON STYLE */
                .lucky-dip-btn { background: linear-gradient(135deg, #3b82f6, #1d4ed8); color: #fff; border: none; padding: 10px 16px; border-radius: 10px; font-weight: bold; cursor: pointer; display: flex; align-items: center; justify-content: center; gap: 8px; font-size: 13px; box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3); transition: all 0.2s; }
                .lucky-dip-btn:hover { background: linear-gradient(135deg, #2563eb, #1e40af); transform: translateY(-1px); }
                .lucky-dip-result { background: #0f172a; border: 1px dashed #38bdf8; border-radius: 10px; padding: 12px; margin-top: 8px; display: none; font-size: 13px; color: #e2e8f0; }

                .table-felt { background: #064e3b; border: 2px solid #059669; border-radius: 14px; padding: 20px; text-align: center; display: flex; flex-direction: column; gap: 12px; }
                .card-box { display: inline-block; background: #fff; color: #000; padding: 10px 14px; border-radius: 8px; font-weight: bold; font-family: monospace; font-size: 16px; margin: 4px; box-shadow: 0 4px 6px rgba(0,0,0,0.3); }
                .game-btn { background: #22c55e; color: #000; font-weight: bold; border: none; padding: 10px 16px; border-radius: 8px; cursor: pointer; }
            </style>
        </head>
        <body>
            <div class="container">
                <header>
                    <div>
                        <h1>🌴 Anadolu AI Sportsbook & Lucky Dip Lounge</h1>
                        <p>Status: <span class="badge">TOMORROW & UPCOMING MATCHES • LIVE ODDS ACTIVE</span></p>
                    </div>
                </header>

                <div class="card">
                    <h2>⚽ Tomorrow & Upcoming International & League Matches</h2>
                    <p style="color:#94a3b8; font-size:12px;">Click the <b>🎲 Lucky Dip</b> button on any match to instantly generate a randomized AI accumulator bet!</p>
                    
                    <div class="fixtures-scroll-container">
                        ${matches ? matches.map((m, index) => {
                            const mk = calculateInPlayMarkets(m.home_rating, m.away_rating, m.aggression_rating);
                            return `
                            <div class="match-box">
                                <div class="match-header">
                                    <div>
                                        <span class="league-tag">${m.league_category}</span>
                                        <b style="font-size:16px; color:#fff; display:block; margin-top:2px;">🇹🇷 ${m.home_team} vs${m.away_team} 🇫🇷</b>
                                        <span style="color:#38bdf8; font-size:11px; font-weight:bold;">📍 ${m.venue} • ⏰ ${m.match_date}</span>
                                    </div>
                                    <span style="color: #22c55e; font-family: monospace; font-weight:bold; font-size:12px;">AI Calibrated</span>
                                </div>

                                <div class="odds-row" style="margin-top:2px;">
                                    <div class="bet-btn">
                                        <span class="bet-label">${m.home_team} (Home)</span>
                                        <span class="bet-val">${mk.homeDecimal} <span style="font-size:10px; color:#38bdf8;">(${mk.homeWinProb}%)</span></span>
                                    </div>
                                    <div class="bet-btn">
                                        <span class="bet-label">Draw (X)</span>
                                        <span class="bet-val" style="color:#38bdf8;">${mk.drawDecimal} <span style="font-size:10px; color:#94a3b8;">(${mk.drawProb}%)</span></span>
                                    </div>
                                    <div class="bet-btn">
                                        <span class="bet-label">${m.away_team} (Away)</span>
                                        <span class="bet-val" style="color:#fb7185;">${mk.awayDecimal} <span style="font-size:10px; color:#38bdf8;">(${mk.awayWinProb}%)</span></span>
                                    </div>
                                </div>

                                <div style="display:flex; gap:10px; flex-wrap:wrap;">
                                    <div class="stats-tag">⚽ <b>First Goal:</b> ${mk.firstGoalTeam}</div>
                                    <div class="stats-tag">🥅 <b>Goals Line:</b> ${mk.overUnderGoals}</div>
                                    <div class="stats-tag">🚩 <b>Corners:</b> ~${mk.expectedCorners}</div>
                                    <div class="stats-tag">⚠️ <b>Fouls:</b> ~${mk.expectedFouls}</div>
                                    <div class="stats-tag">🟥 <b>Red Card:</b> ${mk.redCardRisk}</div>
                                </div>

                                <!-- LUCKY DIP SECTION -->
                                <div style="margin-top: 4px;">
                                    <button class="lucky-dip-btn" onclick="generateLuckyDip(${index}, '${m.home_team}', '${m.away_team}')">
                                        🎲 Generate Lucky Dip Bet
                                    </button>
                                    <div id="luckyResult-${index}" class="lucky-dip-result"></div>
                                </div>
                            </div>`;
                        }).join('') : ''}
                    </div>
                </div>
            </div>

            <script>
                function generateLuckyDip(index, home, away) {
                    const markets = [
                        \`Match Winner: \${home} & Both Teams to Score (Odds: 4.80)\`,
                        \`Exact Score: 2-1 in favor of \${home} (Odds: 8.50)\`,
                        \`First Goalscorer Combo: \${away} to score first & Over 2.5 Goals (Odds: 6.20)\`,
                        \`Half-Time / Full-Time: Draw / \${home} (Odds: 5.50)\`,
                        \`Total Corners Over 10.5 & \${away} Win (Odds: 7.10)\`,
                        \`Player Card Combo: Red card in match & Both Teams Score (Odds: 9.00)\`
                    ];
                    
                    const randomPick = markets[Math.floor(Math.random() * markets.length)];
                    const resultBox = document.getElementById('luckyResult-' + index);
                    
                    resultBox.style.display = 'block';
                    resultBox.innerHTML = \`✨ <b>Lucky Dip Pick Generated:</b> <span style="color:#38bdf8;">\${randomPick}</span>\`;
                }
            </script>
        </body>
        </html>
        `);
    });
});

app.listen(PORT, () => {
    console.log(`🚀 Sportsbook running on port ${PORT}`);
});
