PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;
CREATE TABLE audit_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_email TEXT,
            event_type TEXT NOT NULL,
            event_detail TEXT NOT NULL,
            ip_address TEXT NOT NULL DEFAULT 'N/A',
            user_agent TEXT NOT NULL DEFAULT 'N/A',
            created_at TEXT NOT NULL DEFAULT (datetime('now')),
            FOREIGN KEY (user_email) REFERENCES users(email) ON DELETE SET NULL
        );
CREATE TABLE debts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_email TEXT NOT NULL,
            name TEXT NOT NULL,
            total_amount REAL NOT NULL CHECK (total_amount >= 0),
            paid_amount REAL NOT NULL DEFAULT 0,
            due_date TEXT,
            status TEXT NOT NULL DEFAULT 'active' CHECK (status IN ('active', 'paid')),
            created_at TEXT NOT NULL DEFAULT (datetime('now')),
            updated_at TEXT NOT NULL DEFAULT (datetime('now')),
            FOREIGN KEY (user_email) REFERENCES users(email) ON DELETE CASCADE
        );
CREATE TABLE investments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_email TEXT,
        symbol TEXT NOT NULL,
        name TEXT NOT NULL,
        investment REAL NOT NULL,
        current REAL NOT NULL,
        pnl REAL NOT NULL,
        type TEXT NOT NULL,
        FOREIGN KEY (user_email) REFERENCES users (email)
    );
INSERT INTO "investments" VALUES(1,'admin@financepro.com','BTC','Bitcoin',5000.0,5450.25,9.01,'crypto');
INSERT INTO "investments" VALUES(2,'admin@financepro.com','AAPL','Apple Inc.',2000.0,1890.4,-5.48,'stock');
INSERT INTO "investments" VALUES(3,'orozcoreinaldo610@gmail.com','BTCC','btcc',10.0,10.0,0.0,'stock');
INSERT INTO "investments" VALUES(4,'admin@financepro.com','BTC','Bitcoin',5000.0,5450.25,9.01,'crypto');
INSERT INTO "investments" VALUES(5,'admin@financepro.com','AAPL','Apple Inc.',2000.0,1890.4,-5.48,'stock');
INSERT INTO "investments" VALUES(6,'orozcoreinaldo610@gmail.com','BTCC','btcc',10.0,10.0,0.0,'stock');
CREATE TABLE market_assets (
            symbol TEXT PRIMARY KEY,
            display_name TEXT NOT NULL,
            asset_class TEXT NOT NULL,
            price REAL NOT NULL,
            change_percent REAL NOT NULL DEFAULT 0,
            updated_at TEXT NOT NULL DEFAULT (datetime('now'))
        );
INSERT INTO "market_assets" VALUES('BTC','Bitcoin','crypto',44120.5,2.45,'2026-03-15T16:35:39.921946+00:00');
INSERT INTO "market_assets" VALUES('ETH','Ethereum','crypto',2450.12,1.2,'2026-03-15T16:35:39.921946+00:00');
INSERT INTO "market_assets" VALUES('SPX','S&P 500','index',4890.97,0.85,'2026-03-15T16:35:39.921946+00:00');
INSERT INTO "market_assets" VALUES('AAPL','Apple Inc.','stock',189.43,-1.12,'2026-03-15T16:35:39.921946+00:00');
CREATE TABLE movements (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_email TEXT,
        type TEXT NOT NULL,
        concept TEXT NOT NULL,
        amount REAL NOT NULL,
        date TEXT NOT NULL,
        category TEXT NOT NULL,
        FOREIGN KEY (user_email) REFERENCES users (email)
    );
INSERT INTO "movements" VALUES(1,'admin@financepro.com','income','Monthly Salary',5000.0,'2026-02-20','Salary');
INSERT INTO "movements" VALUES(2,'admin@financepro.com','expense','February Rent',1200.0,'2026-02-21','Rent');
INSERT INTO "movements" VALUES(3,'admin@financepro.com','expense','Groceries',450.0,'2026-02-22','Food');
INSERT INTO "movements" VALUES(4,'orozcoreinaldo610@gmail.com','expense','renta',10.0,'2026-02-25','Servicios');
INSERT INTO "movements" VALUES(5,'admin@financepro.com','income','Monthly Salary',5000.0,'2026-02-20','Salary');
INSERT INTO "movements" VALUES(6,'admin@financepro.com','expense','February Rent',1200.0,'2026-02-21','Rent');
INSERT INTO "movements" VALUES(7,'admin@financepro.com','expense','Groceries',450.0,'2026-02-22','Food');
INSERT INTO "movements" VALUES(8,'orozcoreinaldo610@gmail.com','expense','renta',10.0,'2026-02-25','Servicios');
INSERT INTO "movements" VALUES(9,'garciaorozcojose12@gmail.com','expense','pago nomina ',100000.0,'2026-03-09','Otros');
INSERT INTO "movements" VALUES(10,'lolojaja265@gmail.com','expense','pago nomina ',200000.0,'2026-03-10','Otros');
INSERT INTO "movements" VALUES(11,'lolojaja265@gmail.com','income','invercion',1000000.0,'2026-03-10','Alimentación');
INSERT INTO "movements" VALUES(12,'orozcoreinaldo610@gmail.com','income','vents',200000.0,'2026-03-12','Stock');
INSERT INTO "movements" VALUES(13,'orozcoreinaldo610@gmail.com','expense','pago',1000000000.0,'2026-03-13','Hogar');
CREATE TABLE news_articles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category TEXT NOT NULL,
            source TEXT NOT NULL,
            title TEXT NOT NULL,
            summary TEXT NOT NULL,
            image_url TEXT NOT NULL,
            article_url TEXT NOT NULL UNIQUE,
            published_at TEXT NOT NULL,
            created_at TEXT NOT NULL DEFAULT (datetime('now'))
        );
INSERT INTO "news_articles" VALUES(1,'Crypto','Financial Times','Bitcoin Surges Past $44,000 as Institutional Interest Peaks','ETF expectations and halving narratives keep Bitcoin demand elevated across institutional desks.','https://images.unsplash.com/photo-1518546305927-5a555bb7020d?auto=format&fit=crop&w=800&q=80','https://example.com/news/bitcoin-44000','2026-03-01T18:51:14.613879+00:00','2026-03-01 18:51:14');
INSERT INTO "news_articles" VALUES(2,'Economy','WSJ','Fed Signals Potential Rate Cuts in Late 2026','Cooling inflation metrics increase probability of a softer monetary policy path.','https://images.unsplash.com/photo-1611974717483-9b939c0e0b57?auto=format&fit=crop&w=800&q=80','https://example.com/news/fed-rate-cuts-2026','2026-03-01T18:51:14.613879+00:00','2026-03-01 18:51:14');
INSERT INTO "news_articles" VALUES(3,'Tech','Bloomberg','NVIDIA Market Cap Hits New Historic Record','AI demand accelerates semiconductor revenues, sending valuation metrics to new highs.','https://images.unsplash.com/photo-1543286386-713bdd548da4?auto=format&fit=crop&w=800&q=80','https://example.com/news/nvidia-record','2026-03-01T18:51:14.613879+00:00','2026-03-01 18:51:14');
CREATE TABLE notifications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_email TEXT NOT NULL,
            type TEXT NOT NULL,
            title TEXT NOT NULL,
            message TEXT NOT NULL,
            is_read INTEGER NOT NULL DEFAULT 0 CHECK (is_read IN (0, 1)),
            created_at TEXT NOT NULL DEFAULT (datetime('now')),
            FOREIGN KEY (user_email) REFERENCES users(email) ON DELETE CASCADE
        );
CREATE TABLE payments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_email TEXT NOT NULL,
            name TEXT NOT NULL,
            amount REAL NOT NULL CHECK (amount >= 0),
            due_date TEXT,
            status TEXT NOT NULL DEFAULT 'pending' CHECK (status IN ('pending', 'completed')),
            created_at TEXT NOT NULL DEFAULT (datetime('now')),
            updated_at TEXT NOT NULL DEFAULT (datetime('now')),
            FOREIGN KEY (user_email) REFERENCES users(email) ON DELETE CASCADE
        );
CREATE TABLE portfolio_snapshots (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_email TEXT NOT NULL,
            snapshot_date TEXT NOT NULL,
            net_worth REAL NOT NULL DEFAULT 0,
            liquid_balance REAL NOT NULL DEFAULT 0,
            invested_value REAL NOT NULL DEFAULT 0,
            daily_change_percent REAL NOT NULL DEFAULT 0,
            created_at TEXT NOT NULL DEFAULT (datetime('now')),
            UNIQUE (user_email, snapshot_date),
            FOREIGN KEY (user_email) REFERENCES users(email) ON DELETE CASCADE
        );
CREATE TABLE user_profiles (
            user_email TEXT PRIMARY KEY,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL DEFAULT '',
            bio TEXT NOT NULL DEFAULT '',
            avatar_url TEXT NOT NULL DEFAULT '',
            membership_level TEXT NOT NULL DEFAULT 'PREMIUM',
            joined_at TEXT NOT NULL DEFAULT (datetime('now')),
            country TEXT NOT NULL DEFAULT 'N/A',
            timezone TEXT NOT NULL DEFAULT 'UTC',
            language TEXT NOT NULL DEFAULT 'es',
            created_at TEXT NOT NULL DEFAULT (datetime('now')),
            updated_at TEXT NOT NULL DEFAULT (datetime('now')), phone_number TEXT NOT NULL DEFAULT '',
            FOREIGN KEY (user_email) REFERENCES users(email) ON DELETE CASCADE
        );
INSERT INTO "user_profiles" VALUES('admin@financepro.com','Admin','User','','','PREMIUM','2026-03-01T18:51:14.536551+00:00','N/A','UTC','es','2026-03-01T18:51:14.536551+00:00','2026-03-01T18:51:14.536551+00:00','');
INSERT INTO "user_profiles" VALUES('orozcoreinaldo610@gmail.com','reinaldo','orozco','','','PREMIUM','2026-03-01T18:51:14.550121+00:00','N/A','UTC','es','2026-03-01T18:51:14.550121+00:00','2026-03-01T18:51:14.550121+00:00','');
INSERT INTO "user_profiles" VALUES('leisypaolaorozcogarcia@gmail.com','rei','jos','','','PREMIUM','2026-03-01T18:51:14.620218+00:00','N/A','UTC','es','2026-03-01T18:51:14.620218+00:00','2026-03-01T18:51:14.620218+00:00','');
INSERT INTO "user_profiles" VALUES('leisypaolaorozogarcia@gmail.com','rei','jos','','','PREMIUM','2026-03-01T18:51:14.621160+00:00','N/A','UTC','es','2026-03-01T18:51:14.621160+00:00','2026-03-01T18:51:14.621160+00:00','');
INSERT INTO "user_profiles" VALUES('admin@Aplicativo Web para el Manejo de Finanzas Personales.com','Admin','User','','','PREMIUM','2026-03-12T15:25:15.108972+00:00','N/A','UTC','es','2026-03-12T15:25:15.108972+00:00','2026-03-12T15:25:15.108972+00:00','');
INSERT INTO "user_profiles" VALUES('kinm34496@gmail.com','kinm34496','','','','PREMIUM','2026-03-14 17:13:30','N/A','UTC','es','2026-03-14 17:13:30','2026-03-14 17:13:30','+57 3229620293');
CREATE TABLE user_settings (
            user_email TEXT PRIMARY KEY,
            currency TEXT NOT NULL DEFAULT 'USD',
            dynamic_dark_mode INTEGER NOT NULL DEFAULT 1 CHECK (dynamic_dark_mode IN (0, 1)),
            two_factor_enabled INTEGER NOT NULL DEFAULT 0 CHECK (two_factor_enabled IN (0, 1)),
            market_alerts_enabled INTEGER NOT NULL DEFAULT 1 CHECK (market_alerts_enabled IN (0, 1)),
            weekly_summary_enabled INTEGER NOT NULL DEFAULT 1 CHECK (weekly_summary_enabled IN (0, 1)),
            crypto_news_enabled INTEGER NOT NULL DEFAULT 0 CHECK (crypto_news_enabled IN (0, 1)),
            new_device_alerts_enabled INTEGER NOT NULL DEFAULT 0 CHECK (new_device_alerts_enabled IN (0, 1)),
            created_at TEXT NOT NULL DEFAULT (datetime('now')),
            updated_at TEXT NOT NULL DEFAULT (datetime('now')),
            FOREIGN KEY (user_email) REFERENCES users(email) ON DELETE CASCADE
        );
INSERT INTO "user_settings" VALUES('admin@financepro.com','USD',1,0,1,1,0,0,'2026-03-01T18:51:14.536551+00:00','2026-03-01T18:51:14.536551+00:00');
INSERT INTO "user_settings" VALUES('orozcoreinaldo610@gmail.com','USD',1,0,1,1,0,0,'2026-03-01T18:51:14.550121+00:00','2026-03-01T18:51:14.550121+00:00');
INSERT INTO "user_settings" VALUES('leisypaolaorozcogarcia@gmail.com','USD',1,0,1,1,0,0,'2026-03-01T18:51:14.620218+00:00','2026-03-01T18:51:14.620218+00:00');
INSERT INTO "user_settings" VALUES('leisypaolaorozogarcia@gmail.com','USD',1,0,1,1,0,0,'2026-03-01T18:51:14.621160+00:00','2026-03-01T18:51:14.621160+00:00');
INSERT INTO "user_settings" VALUES('admin@Aplicativo Web para el Manejo de Finanzas Personales.com','USD',1,0,1,1,0,0,'2026-03-12T15:25:15.108972+00:00','2026-03-12T15:25:15.108972+00:00');
CREATE TABLE users (
        email TEXT PRIMARY KEY,
        password TEXT NOT NULL,
        name TEXT NOT NULL,
        is_new INTEGER DEFAULT 1
    , phone TEXT);
INSERT INTO "users" VALUES('admin@financepro.com','password123','Admin User',0,NULL);
INSERT INTO "users" VALUES('orozcoreinaldo610@gmail.com','31062007','reinaldo orozco',1,NULL);
INSERT INTO "users" VALUES('leisypaolaorozcogarcia@gmail.com','mttm4kt','rei  jos',1,NULL);
INSERT INTO "users" VALUES('leisypaolaorozogarcia@gmail.com','12345','rei  jos',1,NULL);
INSERT INTO "users" VALUES('admin@Aplicativo Web para el Manejo de Finanzas Personales.com','password123','Admin User',0,NULL);
CREATE TABLE verification_codes (
            email TEXT PRIMARY KEY,
            code TEXT NOT NULL,
            expires_at TEXT NOT NULL,
            FOREIGN KEY (email) REFERENCES users(email) ON DELETE CASCADE
        );
CREATE INDEX idx_movements_user_date ON movements(user_email, date DESC);
CREATE INDEX idx_investments_user ON investments(user_email);
CREATE INDEX idx_notifications_user_read ON notifications(user_email, is_read);
CREATE INDEX idx_news_category_date ON news_articles(category, published_at DESC);
DELETE FROM "sqlite_sequence";
INSERT INTO "sqlite_sequence" VALUES('movements',13);
INSERT INTO "sqlite_sequence" VALUES('investments',6);
INSERT INTO "sqlite_sequence" VALUES('news_articles',87);
COMMIT;
