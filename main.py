/**
 * ==============================================================================
 * SOVEREIGN MUSIC & CULTURE HUNTER ENGINE
 * (Pop, Hip-Hop, Automated RSS Feeds, & Affiliate Tracking)
 * ==============================================================================
 */

const express = require('express');
const sqlite3 = require('sqlite3').verbose();
const path = require('path');
const Parser = require('rss-parser');

const app = express();
const rssParser = new Parser();
const PORT = process.env.PORT || 10000;

app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// Enable CORS for mobile companion apps & PWA
app.use((req, res, next) => {
    res.header('Access-Control-Allow-Origin', '*');
    res.header('Access-Control-Allow-Headers', 'Origin, X-Requested-With, Content-Type, Accept');
    next();
});

// ==============================================================================
// 1. DATABASE INITIALIZATION & MUSIC CULTURE TABLES
// ==============================================================================
const dbFile = path.join(__dirname, 'sovereign_master.db');
const db = new sqlite3.Database(dbFile, (err) => {
    if (err) {
        console.error('❌ Database error:', err.message);
    } else {
        console.log('✅ Connected to Sovereign Music DB.');
        initializeMusicEngine();
    }
});

function initializeMusicEngine() {
    db.serialize(() => {
        // System Logs
        db.run(`CREATE TABLE IF NOT EXISTS system_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            module_name TEXT,
            status TEXT,
            message TEXT
        )`);

        // Harvested Music Drops & Deals Feed
        db.run(`CREATE TABLE IF NOT EXISTS harvested_music (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            title TEXT,
            link TEXT,
            genre TEXT,
            source_feed TEXT,
            status TEXT DEFAULT 'ACTIVE'
        )`, () => {
            db.get(`SELECT COUNT(*) as count FROM harvested_music`, (err, row) => {
                if (row && row.count === 0) {
                    db.run(`INSERT INTO harvested_music (title, link, genre, source_feed, status) VALUES 
                        ('Kendrick Lamar - New Stadium Tour & Vinyl Drop', 'https://www.amazon.com/s?k=Kendrick+Lamar+vinyl&tag=mrcenk20-21', 'Hip-Hop', 'Culture Radar', 'TAGGED (mrcenk20-21)'),
                        ('Top Pop Anthems 2026 - Collector Edition Vinyl', 'https://www.amazon.com/s?k=Pop+music+vinyl+records&tag=mrcenk20-21', 'Pop', 'Global Charts', 'TAGGED (mrcenk20-21)'),
                        ('Studio Headphone & Audio Gear Deals', 'https://www.amazon.com/s?k=studio+headphones+music&tag=mrcenk20-21', 'Production', 'Gear Hunter', 'TAGGED (mrcenk20-21)')`);
                }
            });
        });

        // Blueprint Registry
        db.run(`CREATE TABLE IF NOT EXISTS blueprint_registry (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            blueprint_id TEXT,
            title TEXT,
            category TEXT,
            status TEXT,
            notes TEXT
        )`, () => {
            db.get(`SELECT COUNT(*) as count FROM blueprint_registry`, (err, row) => {
                if (row && row.count === 0) {
                    db.run(`INSERT INTO blueprint_registry (blueprint_id, title, category, status, notes) VALUES 
                        ('BP-M01', 'Hip-Hop & Pop Culture Radar', 'Music Engine', 'ACTIVE', 'Automated RSS & music gear harvesting active.'),
                        ('BP-M02', 'Mobile Audio PWA Stream', 'Mobile', 'READY', 'JSON endpoints live for mobile client pairing.'),
                        ('BP-M03', 'Affiliate Tag Injector (mrcenk20-21)', 'Monetization', 'ACTIVE', 'Amazon Associate tag automatically appended to links.')`);
                }
            });
        });
    });
}

function logEvent(module, status, message) {
    try {
        const stmt = db.prepare(`INSERT INTO system_logs (module_name, status, message) VALUES (?, ?, ?)`);
        stmt.run(module, status, message);
        stmt.finalize();
    } catch (e) {
        console.error('Log error:', e.message);
    }
}

// ==============================================================================
// 2. BACKGROUND MUSIC & CULTURE HUNTER WORKER
// ==============================================================================
async function runMusicHunterWorker() {
    const feedUrl = 'https://news.google.com/rss/search?q=hip+hop+pop+music+vinyl+releases&hl=en-US&gl=US&ceid=US:en';
    try {
        const feed = await rssParser.parseURL(feedUrl);
        let count = 0;
        for (let item of feed.items.slice(0, 3)) {
            let targetLink = item.link;
            if (targetLink.includes('amazon.com') && !targetLink.includes('tag=')) {
                targetLink += (targetLink.includes('?') ? '&' : '?') + 'tag=mrcenk20-21';
            } else if (!targetLink.includes('tag=')) {
                // Default search redirect for non-affiliate links to monetize through affiliate gear/music
                targetLink = `https://www.amazon.com/s?k=${encodeURIComponent(item.title.slice(0, 25))}&tag=mrcenk20-21`;
            }

            db.run(`INSERT INTO harvested_music (title, link, genre, source_feed, status) VALUES (?, ?, ?, ?, ?)`,
                [item.title, targetLink, 'Hip-Hop / Pop', feed.title || 'Music RSS Stream', 'TAGGED (mrcenk20-21)']);
            count++;
        }
        logEvent('MusicHunter', 'SUCCESS', `Harvested ${count} new music culture drops.`);
        console.log(`🎵 Music Hunter Worker: Harvested ${count} items.`);
    } catch (err) {
        logEvent('MusicHunter', 'ERROR', `Music poll failed: ${err.message}`);
    }
}

// Run music hunter loop every hour
setInterval(runMusicHunterWorker, 60 * 60 * 1000);

// ==============================================================================
// 3. API ENDPOINTS
// ==============================================================================

// JSON API for Mobile Client / PWA
app.get('/api/mobile/music-feed', (req, res) => {
    db.all(`SELECT * FROM harvested_music ORDER BY timestamp DESC LIMIT 10`, [], (err, tracks) => {
        if (err) return res.status(500).json({ error: err.message });
        res.json({
            status: 'success',
            platform: 'Sovereign Music & Culture Engine',
            associates_id: 'mrcenk20-21',
            tracks: tracks
        });
    });
});

// Manual Injector for specific drops (e.g. Kendrick, Pop hits, vinyl)
app.post('/api/music/inject', (req, res) => {
    const { title, link, genre } = req.body;
    let finalLink = link || 'https://www.amazon.com/s?k=music&tag=mrcenk20-21';
    if (finalLink.includes('amazon.com') && !finalLink.includes('tag=')) {
        finalLink += (finalLink.includes('?') ? '&' : '?') + 'tag=mrcenk20-21';
    }

    db.run(`INSERT INTO harvested_music (title, link, genre, source_feed, status) VALUES (?, ?, ?, ?, ?)`,
        [title || 'Exclusive Hip-Hop / Pop Drop', finalLink, genre || 'Hip-Hop', 'Manual Injector', 'TAGGED (mrcenk20-21)'], (err) => {
            if (err) return res.status(500).json({ status: 'error', message: err.message });
            logEvent('ManualInjector', 'SUCCESS', `Injected music drop: [${title}]`);
            res.json({ status: 'success', tag: 'mrcenk20-21' });
        });
});

// ==============================================================================
// 4. MASTER MUSIC COMMAND CENTER DASHBOARD
// ==============================================================================
app.get('/', (req, res) => {
    db.all(`SELECT * FROM blueprint_registry`, [], (errBP, blueprints) => {
        db.all(`SELECT * FROM harvested_music ORDER BY timestamp DESC LIMIT 8`, [], (errTracks, tracks) => {
            db.all(`SELECT * FROM system_logs ORDER BY timestamp DESC LIMIT 5`, [], (errLogs, logs) => {
                
                res.send(`
                <!DOCTYPE html>
                <html lang="en">
                <head>
                    <meta charset="UTF-8">
                    <title>Sovereign Music & Culture Engine</title>
                    <style>
                        * { box-sizing: border-box; margin: 0; padding: 0; }
                        body { font-family: -apple-system, sans-serif; background: #0a0c0b; color: #f1f5f9; padding: 25px; }
                        .container { max-width: 1100px; margin: 0 auto; display: flex; flex-direction: column; gap: 22px; }
                        header { background: #121e16; padding: 24px; border-radius: 18px; border: 1px solid rgba(34, 197, 94, 0.4); display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 15px; }
                        h1 { color: #22c55e; font-size: 24px; margin-bottom: 4px; }
                        .badge { background: #22c55e; color: #000; padding: 5px 14px; border-radius: 20px; font-weight: bold; font-size: 12px; }
                        .card { background: #121e16; border: 1px solid rgba(255,255,255,0.08); border-radius: 18px; padding: 22px; }
                        h2 { font-size: 17px; color: #fff; margin-bottom: 14px; }
                        table { width: 100%; border-collapse: collapse; margin-top: 8px; }
                        th, td { text-align: left; padding: 12px; border-bottom: 1px solid rgba(255,255,255,0.06); font-size: 13px; }
                        th { color: #94a3b8; }
                        .form-group { display: flex; gap: 10px; margin-top: 12px; flex-wrap: wrap; }
                        input, select { background: #18281d; border: 1px solid rgba(34,197,94,0.3); color: #fff; padding: 12px; border-radius: 10px; font-size: 13px; flex: 1; min-width: 200px; }
                        button { background: #22c55e; color: #000; font-weight: bold; padding: 12px 20px; border: none; border-radius: 10px; cursor: pointer; font-size: 13px; }
                        button:hover { opacity: 0.9; }
                    </style>
                </head>
                <body>
                    <div class="container">
                        <header>
                            <div>
                                <h1>🎧 Sovereign Music & Culture Engine</h1>
                                <p>Status: <span class="badge">HIP-HOP & POP RADAR ACTIVE</span> | Associate ID: <code>mrcenk20-21</code></p>
                            </div>
                        </header>

                        <!-- Manual Music / Drop Injector -->
                        <div class="card">
                            <h2>⚡ Inject Music Drop, Vinyl, or Gear (Auto-Tagged)</h2>
                            <form action="/api/music/inject" method="POST" class="form-group">
                                <input type="text" name="title" placeholder="Drop Title (e.g., Kendrick Lamar Exclusive / Pop Vinyl)" required>
                                <input type="text" name="link" placeholder="Destination Link (Amazon / Store URL)" required>
                                <select name="genre">
                                    <option value="Hip-Hop">Hip-Hop</option>
                                    <option value="Pop">Pop</option>
                                    <option value="Gear">Studio / Audio Gear</option>
                                </select>
                                <button type="submit">Publish & Tag (mrcenk20-21)</button>
                            </form>
                        </div>

                        <!-- Live Music Stream -->
                        <div class="card">
                            <h2>🔥 Live Music & Culture Stream (Auto-Tagged with mrcenk20-21)</h2>
                            <table>
                                <tr><th>Timestamp</th><th>Genre</th><th>Drop Title & Link</th><th>Status</th></tr>
                                ${tracks ? tracks.map(t => `
                                    <tr>
                                        <td>${t.timestamp}</td>
                                        <td><span style="color:#38bdf8; font-weight:bold;">${t.genre}</span></td>
                                        <td><a href="${t.link}" target="_blank" style="color:#22c55e; text-decoration:none; font-weight:bold;">${t.title}</a></td>
                                        <td style="color:#94a3b8;">${t.status}</td>
                                    </tr>
                                `).join('') : ''}
                            </table>
                        </div>

                        <!-- Blueprint Registry -->
                        <div class="card">
                            <h2>🗺️ Music Engine Architecture Registry</h2>
                            <table>
                                <tr><th>ID</th><th>Title</th><th>Category</th><th>Status</th><th>Notes</th></tr>
                                ${blueprints ? blueprints.map(b => `
                                    <tr>
                                        <td><b>${b.blueprint_id}</b></td>
                                        <td>${b.title}</td>
                                        <td><span style="color:#38bdf8;">${b.category}</span></td>
                                        <td><span style="color:#22c55e; font-weight:bold;">${b.status}</span></td>
                                        <td>${b.notes}</td>
                                    </tr>
                                `).join('') : ''}
                            </table>
                        </div>

                        <!-- System Telemetry -->
                        <div class="card">
                            <h2>📋 System Telemetry Logs</h2>
                            <table>
                                <tr><th>Timestamp</th><th>Module</th><th>Status</th><th>Message</th></tr>
                                ${logs ? logs.map(l => `<tr><td>${l.timestamp}</td><td>${l.module_name}</td><td style="color:#38bdf8;">${l.status}</td><td>${l.message}</td></tr>`).join('') : ''}
                            </table>
                        </div>
                    </div>
                </body>
                </html>
                `);
            });
        });
    });
});

app.listen(PORT, () => {
    console.log(`🚀 Sovereign Music & Culture Engine running on port ${PORT}`);
    runMusicHunterWorker();
});
