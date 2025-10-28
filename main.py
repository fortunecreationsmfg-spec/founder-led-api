from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
async def root():
    return """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="Founder-Led + Network Effects Investment Strategy App">
    <meta name="theme-color" content="#2563eb">
    <link rel="manifest" href="data:application/json;base64,eyJuYW1lIjoiRm91bmRlci1MZWQgSW52ZXN0bWVudHMiLCJzaG9ydF9uYW1lIjoiRm91bmRlci1MZWQiLCJkZXNjcmlwdGlvbiI6IlRyYWNrIGZvdW5kZXItbGVkIGNvbXBhbmllcyB3aXRoIG5ldHdvcmsgZWZmZWN0cyIsInN0YXJ0X3VybCI6Ii8iLCJkaXNwbGF5Ijoic3RhbmRhbG9uZSIsImJhY2tncm91bmRfY29sb3IiOiIjZmZmZmZmIiwidGhlbWVfY29sb3IiOiIjMjU2M2ViIn0=">
    <title>Founder-Led Investments</title>
    
    <!-- Google tag (gtag.js) -->
    <script async src="https://www.googletagmanager.com/gtag/js?id=G-4DE6DDYBBE"></script>
    <script>
      window.dataLayer = window.dataLayer || [];
      function gtag(){dataLayer.push(arguments);}
      gtag('js', new Date());
      gtag('config', 'G-4DE6DDYBBE');
    </script>
    <script src="https://cdn.tailwindcss.com"></script>
    <script crossorigin src="https://unpkg.com/react@18/umd/react.production.min.js"></script>
    <script crossorigin src="https://unpkg.com/react-dom@18/umd/react-dom.production.min.js"></script>
    <script src="https://unpkg.com/@babel/standalone/babel.min.js"></script>
    <style>
        body { margin: 0; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', sans-serif; }
        .install-prompt {
            position: fixed;
            bottom: 20px;
            left: 50%;
            transform: translateX(-50%);
            background: #2563eb;
            color: white;
            padding: 16px 24px;
            border-radius: 12px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.3);
            z-index: 9999;
            display: none;
            align-items: center;
            gap: 12px;
        }
        .install-prompt.show { display: flex; }
        .install-prompt button {
            background: white;
            color: #2563eb;
            border: none;
            padding: 8px 16px;
            border-radius: 6px;
            font-weight: bold;
            cursor: pointer;
        }
    </style>
</head>
<body>
    <div id="root"></div>
    
    <div class="install-prompt" id="installPrompt">
        📱 Install app on your home screen!
        <button onclick="installApp()">Install</button>
        <button onclick="dismissInstall()" style="background: transparent; color: white;">✕</button>
    </div>

    <script type="text/babel">
        const { useState, useEffect, useMemo } = React;

        // API service
        const API_BASE_URL = 'https://founder-led-api-production.up.railway.app/api';

        function App() {
            const [companies, setCompanies] = useState([]);
            const [topTwenty, setTopTwenty] = useState([]);
            const [topSeven, setTopSeven] = useState([]);
            const [inverseCramer, setInverseCramer] = useState(null);
            const [selectedTab, setSelectedTab] = useState(0);
            const [loading, setLoading] = useState(true);
            const [networkEffects, setNetworkEffects] = useState(1);
            const [founderLeadership, setFounderLeadership] = useState(1);
            const [selectedCompany, setSelectedCompany] = useState(null);

            useEffect(() => {
                fetchData();
            }, []);

            const fetchData = async () => {
                setLoading(true);
                try {
                    const response = await fetch(`${API_BASE_URL}/companies`);
                    const data = await response.json();
                    setCompanies(data);
                } catch (error) {
                    console.error('Error fetching data:', error);
                }
                setLoading(false);
            };

            const fetchTopTwenty = async () => {
                try {
                    const response = await fetch(`${API_BASE_URL}/top-twenty`);
                    const data = await response.json();
                    setTopTwenty(data);
                } catch (error) {
                    console.error('Error:', error);
                }
            };

            const fetchTopSeven = async () => {
                try {
                    const response = await fetch(`${API_BASE_URL}/top-seven`);
                    const data = await response.json();
                    setTopSeven(data);
                } catch (error) {
                    console.error('Error:', error);
                }
            };

            const fetchInverseCramer = async () => {
                try {
                    const response = await fetch(`${API_BASE_URL}/inverse-cramer`);
                    const data = await response.json();
                    setInverseCramer(data);
                } catch (error) {
                    console.error('Error:', error);
                }
            };

            const filteredCompanies = useMemo(() => {
                return companies.filter(c => 
                    c.network_effects_rank >= networkEffects &&
                    c.founder_leadership_rank >= founderLeadership
                );
            }, [companies, networkEffects, founderLeadership]);

            const getRecColor = (action) => {
                if (action === 'BUY') return 'bg-green-100 text-green-700';
                if (action === 'SELL') return 'bg-red-100 text-red-700';
                return 'bg-yellow-100 text-yellow-700';
            };

            return (
                <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-50">
                    {/* Header */}
                    <div className="bg-gradient-to-r from-blue-600 to-indigo-600 text-white p-6 shadow-lg">
                        <div className="max-w-6xl mx-auto">
                            <div className="flex items-center space-x-3">
                                <svg className="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6" />
                                </svg>
                                <div>
                                    <h1 className="text-2xl font-bold">Founder-Led + Network Effects</h1>
                                    <p className="text-blue-100 text-sm">Companies that outperform by 3.1x</p>
                                </div>
                            </div>
                        </div>
                    </div>

                    {/* Tabs */}
                    <div className="max-w-6xl mx-auto px-6 pt-6">
                        <div className="flex space-x-2 mb-4">
                            <button
                                onClick={() => setSelectedTab(0)}
                                className={`px-6 py-3 rounded-lg font-semibold transition ${selectedTab === 0 ? 'bg-white text-blue-600 shadow' : 'bg-white/50 text-gray-600'}`}
                            >
                                Founder-Led Strategy
                            </button>
                            <button
                                onClick={() => { setSelectedTab(1); fetchInverseCramer(); }}
                                className={`px-6 py-3 rounded-lg font-semibold transition ${selectedTab === 1 ? 'bg-white text-red-600 shadow' : 'bg-white/50 text-gray-600'}`}
                            >
                                📺 Inverse Cramer
                            </button>
                            <button
                                onClick={() => { setSelectedTab(2); fetchTopSeven(); }}
                                className={`px-6 py-3 rounded-lg font-semibold transition ${selectedTab === 2 ? 'bg-white text-green-600 shadow' : 'bg-white/50 text-gray-600'}`}
                            >
                                🏆 Top Seven
                            </button>
                        </div>

                        {/* Banner */}
                        {selectedTab === 0 && (
                            <div className="bg-gradient-to-r from-green-50 to-emerald-50 border-l-4 border-green-500 rounded-lg p-6 mb-6">
                                <h3 className="text-lg font-bold mb-2">The Winning Formula</h3>
                                <p className="text-gray-700">Network Effects + Founder Leadership = Market Outperformance</p>
                            </div>
                        )}
                        {selectedTab === 1 && (
                            <div className="bg-gradient-to-r from-red-50 to-orange-50 border-l-4 border-red-500 rounded-lg p-6 mb-6">
                                <h3 className="text-lg font-bold mb-2">The Inverse Cramer Effect</h3>
                                <p className="text-gray-700">Do the opposite of Jim Cramer for better returns</p>
                            </div>
                        )}
                        {selectedTab === 2 && (
                            <div className="bg-gradient-to-r from-yellow-50 to-amber-50 border-l-4 border-yellow-500 rounded-lg p-6 mb-6">
                                <h3 className="text-lg font-bold mb-2">Top Seven Strategy</h3>
                                <p className="text-gray-700">Top 7 performers with 200-day MA timing signals</p>
                            </div>
                        )}
                    </div>

                    {/* Content */}
                    <div className="max-w-6xl mx-auto p-6">
                        {loading ? (
                            <div className="text-center py-12">
                                <div className="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
                                <p className="mt-4 text-gray-600">Loading stock data...</p>
                            </div>
                        ) : (
                            <>
                                {selectedTab === 0 && (
                                    <div className="space-y-6">
                                        {/* Filters */}
                                        <div className="bg-white rounded-xl shadow p-6">
                                            <div className="mb-4">
                                                <div className="flex justify-between mb-2">
                                                    <label className="font-semibold">🌐 Network Effects</label>
                                                    <span className="text-blue-600 font-bold">{networkEffects}/10</span>
                                                </div>
                                                <input
                                                    type="range"
                                                    min="1"
                                                    max="10"
                                                    value={networkEffects}
                                                    onChange={(e) => setNetworkEffects(Number(e.target.value))}
                                                    className="w-full"
                                                />
                                            </div>
                                            <div>
                                                <div className="flex justify-between mb-2">
                                                    <label className="font-semibold">👨‍💼 Founder Leadership</label>
                                                    <span className="text-purple-600 font-bold">{founderLeadership}/10</span>
                                                </div>
                                                <input
                                                    type="range"
                                                    min="1"
                                                    max="10"
                                                    value={founderLeadership}
                                                    onChange={(e) => setFounderLeadership(Number(e.target.value))}
                                                    className="w-full"
                                                />
                                            </div>
                                        </div>

                                        {/* Companies */}
                                        <div className="space-y-4">
                                            {filteredCompanies.map(company => (
                                                <div key={company.ticker} className="bg-white rounded-xl shadow p-5 cursor-pointer hover:shadow-lg transition" onClick={() => setSelectedCompany(company)}>
                                                    <div className="flex items-center space-x-3 mb-2">
                                                        <div className="bg-blue-100 text-blue-600 font-bold px-3 py-1 rounded">{company.ticker}</div>
                                                        <h3 className="text-lg font-bold">{company.name}</h3>
                                                        {company.cramer_recommendation === 'sell' && (
                                                            <span className="bg-green-100 text-green-700 text-xs px-2 py-1 rounded font-bold">✅ INVERSE</span>
                                                        )}
                                                    </div>
                                                    <p className="text-sm text-gray-600 mb-3">Founded by {company.founder}</p>
                                                    <div className="grid grid-cols-2 gap-3 text-sm">
                                                        <div>Price: <span className="font-semibold">${company.current_price}</span></div>
                                                        <div>YTD: <span className="font-semibold text-green-600">+{company.ytd_return}%</span></div>
                                                    </div>
                                                </div>
                                            ))}
                                        </div>
                                    </div>
                                )}

                                {selectedTab === 1 && inverseCramer && (
                                    <div className="space-y-6">
                                        <div>
                                            <h3 className="text-xl font-bold text-green-700 mb-4">Cramer Said SELL - Consider BUYING</h3>
                                            {inverseCramer.buy_signals.map(signal => (
                                                <div key={signal.ticker} className="bg-green-50 border-2 border-green-200 rounded-xl p-5 mb-3">
                                                    <div className="flex items-center space-x-3 mb-2">
                                                        <div className="bg-green-600 text-white font-bold px-3 py-1 rounded">{signal.ticker}</div>
                                                        <h3 className="text-lg font-bold">{signal.name}</h3>
                                                    </div>
                                                    <p className="text-sm">Cramer: SELL on {signal.cramer_date}</p>
                                                    <p className="text-xs text-green-700 font-semibold">📈 Inverse opportunity</p>
                                                </div>
                                            ))}
                                        </div>

                                        <div>
                                            <h3 className="text-xl font-bold text-red-700 mb-4">Cramer Said BUY - Be Cautious</h3>
                                            {inverseCramer.avoid_signals.map(signal => (
                                                <div key={signal.ticker} className="bg-red-50 border-2 border-red-200 rounded-xl p-5 mb-3">
                                                    <div className="flex items-center space-x-3 mb-2">
                                                        <div className="bg-red-600 text-white font-bold px-3 py-1 rounded">{signal.ticker}</div>
                                                        <h3 className="text-lg font-bold">{signal.name}</h3>
                                                    </div>
                                                    <p className="text-sm">Cramer: BUY on {signal.cramer_date}</p>
                                                    <p className="text-xs text-red-700 font-semibold">⚠️ Proceed with caution</p>
                                                </div>
                                            ))}
                                        </div>
                                    </div>
                                )}

                                {selectedTab === 2 && (
                                    <div className="space-y-4">
                                        <div className="bg-white rounded-xl shadow p-6">
                                            <h3 className="text-2xl font-bold mb-2">🏆 Top 7 S&P 500 Performers</h3>
                                            <p className="text-gray-600">Ranked by YTD return with 200-day MA signals</p>
                                        </div>

                                        {topSeven.map((stock, index) => (
                                            <div key={stock.ticker} className="bg-white rounded-xl shadow-lg p-6">
                                                <div className="flex items-start justify-between mb-4">
                                                    <div className="flex items-center space-x-4">
                                                        <div className="bg-gradient-to-r from-yellow-400 to-amber-500 text-white font-bold text-2xl w-12 h-12 rounded-full flex items-center justify-center">
                                                            #{index + 1}
                                                        </div>
                                                        <div>
                                                            <div className="flex items-center space-x-3 mb-1">
                                                                <div className="bg-blue-600 text-white font-bold px-3 py-1 rounded">{stock.ticker}</div>
                                                                <h3 className="text-xl font-bold">{stock.name}</h3>
                                                            </div>
                                                            <p className="text-sm">YTD: <span className="font-bold text-green-600">+{stock.ytd_return}%</span></p>
                                                        </div>
                                                    </div>
                                                    <div className={`px-4 py-2 rounded-lg font-bold text-sm ${getRecColor(stock.recommendation.action)}`}>
                                                        {stock.recommendation.action}
                                                    </div>
                                                </div>

                                                <div className="grid grid-cols-3 gap-4 text-sm">
                                                    <div className="bg-blue-50 rounded p-3">
                                                        <div className="text-xs text-gray-600 mb-1">Current Price</div>
                                                        <div className="text-lg font-bold">${stock.current_price}</div>
                                                    </div>
                                                    <div className="bg-purple-50 rounded p-3">
                                                        <div className="text-xs text-gray-600 mb-1">200-Day MA</div>
                                                        <div className="text-lg font-bold">${stock.avg_200_day}</div>
                                                    </div>
                                                    <div className={`rounded p-3 ${stock.recommendation.percent_above_ma > 0 ? 'bg-green-50' : 'bg-red-50'}`}>
                                                        <div className="text-xs text-gray-600 mb-1">vs MA</div>
                                                        <div className={`text-lg font-bold ${stock.recommendation.percent_above_ma > 0 ? 'text-green-700' : 'text-red-700'}`}>
                                                            {stock.recommendation.percent_above_ma > 0 ? '+' : ''}{stock.recommendation.percent_above_ma}%
                                                        </div>
                                                    </div>
                                                </div>
                                            </div>
                                        ))}
                                    </div>
                                )}
                            </>
                        )}
                    </div>

                    {/* Company Detail Modal */}
                    {selectedCompany && (
                        <div className="fixed inset-0 bg-black/50 flex items-center justify-center p-4 z-50" onClick={() => setSelectedCompany(null)}>
                            <div className="bg-white rounded-2xl max-w-2xl w-full p-8" onClick={(e) => e.stopPropagation()}>
                                <div className="flex justify-between items-start mb-6">
                                    <div>
                                        <div className="flex items-center space-x-3 mb-2">
                                            <div className="bg-blue-600 text-white font-bold px-4 py-2 rounded">{selectedCompany.ticker}</div>
                                            <h2 className="text-2xl font-bold">{selectedCompany.name}</h2>
                                        </div>
                                        <p className="text-gray-600">Founded by {selectedCompany.founder}</p>
                                    </div>
                                    <button onClick={() => setSelectedCompany(null)} className="text-gray-400 hover:text-gray-600">✕</button>
                                </div>

                                <div className="grid grid-cols-2 gap-4">
                                    <div className="bg-green-50 p-4 rounded">
                                        <div className="text-sm text-gray-600">Market Cap</div>
                                        <div className="text-2xl font-bold">${selectedCompany.market_cap}B</div>
                                    </div>
                                    <div className="bg-blue-50 p-4 rounded">
                                        <div className="text-sm text-gray-600">YTD Return</div>
                                        <div className="text-2xl font-bold text-green-600">+{selectedCompany.ytd_return}%</div>
                                    </div>
                                    <div className="bg-purple-50 p-4 rounded">
                                        <div className="text-sm text-gray-600">Network Effects</div>
                                        <div className="text-2xl font-bold">{selectedCompany.network_effects_rank}/10</div>
                                    </div>
                                    <div className="bg-orange-50 p-4 rounded">
                                        <div className="text-sm text-gray-600">Founder Leadership</div>
                                        <div className="text-2xl font-bold">{selectedCompany.founder_leadership_rank}/10</div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    )}
                </div>
            );
        }

        ReactDOM.render(<App />, document.getElementById('root'));
    </script>

    <script>
        // PWA Installation
        let deferredPrompt;

        window.addEventListener('beforeinstallprompt', (e) => {
            e.preventDefault();
            deferredPrompt = e;
            document.getElementById('installPrompt').classList.add('show');
        });

        function installApp() {
            if (deferredPrompt) {
                deferredPrompt.prompt();
                deferredPrompt.userChoice.then((choiceResult) => {
                    deferredPrompt = null;
                    document.getElementById('installPrompt').classList.remove('show');
                });
            }
        }

        function dismissInstall() {
            document.getElementById('installPrompt').classList.remove('show');
        }

        // Service Worker for offline support
        if ('serviceWorker' in navigator) {
            window.addEventListener('load', () => {
                const swCode = `
                    self.addEventListener('install', (e) => {
                        e.waitUntil(
                            caches.open('founder-led-v1').then((cache) => {
                                return cache.addAll(['/']);
                            })
                        );
                    });
                    self.addEventListener('fetch', (e) => {
                        e.respondWith(
                            caches.match(e.request).then((response) => {
                                return response || fetch(e.request);
                            })
                        );
                    });
                `;
                const blob = new Blob([swCode], { type: 'application/javascript' });
                const swUrl = URL.createObjectURL(blob);
                navigator.serviceWorker.register(swUrl);
            });
        }
    </script>
</body>
</html>
"""
