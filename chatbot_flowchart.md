# Competitive Intelligence Chatbot — System Flowchart

```mermaid
flowchart TD

    %% ── ENTRY ──────────────────────────────────────────────────
    START([🚀 User visits app]) --> CHECK_SESSION

    %% ── AUTH BLOCK ──────────────────────────────────────────────
    subgraph AUTH ["🔐 Authentication Layer"]
        direction TB
        CHECK_SESSION{Active\nsession?}
        CHECK_ROLE{Role =\nAdmin?}
        LOGIN_PAGE[Render login.html]
        VALIDATE["check_password_hash()\nverify against users.json"]
        CREDS_OK{Credentials\nvalid?}
        SET_SESSION["Set session cookie\nusername + role"]
        LOGIN_ERR["⚠️ flash: Invalid credentials\nRe-render login page"]

        CHECK_SESSION -- NO --> LOGIN_PAGE
        LOGIN_PAGE --> VALIDATE
        VALIDATE --> CREDS_OK
        CREDS_OK -- NO --> LOGIN_ERR
        LOGIN_ERR -.->|retry| LOGIN_PAGE
        CREDS_OK -- YES --> SET_SESSION
        SET_SESSION --> CHECK_ROLE
        CHECK_SESSION -- YES --> CHECK_ROLE
    end

    %% ── ROLE ROUTING ────────────────────────────────────────────
    CHECK_ROLE -- "👤 User" --> CHAT_UI
    CHECK_ROLE -- "🛡️ Admin" --> ADMIN_DASH

    %% ── ADMIN BLOCK ─────────────────────────────────────────────
    subgraph ADMIN ["🗄️ Admin Data Pipeline"]
        direction TB
        ADMIN_DASH[Admin Dashboard\nGET /admin]
        UPLOAD["Upload file\nPOST /admin/upload/{type}"]
        FILE_TYPE{File type?}

        subgraph TABULAR ["Tabular Data"]
            PARSE["pandas read_csv /\nread_excel / json.load\n→ DataFrame"]
            SQLITE["make_table_name()\nload_df_into_sqlite()\n→ In-memory SQLite DB"]
            PARSE --> SQLITE
        end

        subgraph IMAGE_PIPE ["Image Data"]
            PIL["PIL Image.open()\nanalyze_image()\n→ image_text_cache"]
        end

        DATA_READY[("✅ Data in memory\n(sqlite_tables populated)")]

        ADMIN_DASH --> UPLOAD
        UPLOAD --> FILE_TYPE
        FILE_TYPE -- "CSV/Excel/JSON" --> PARSE
        FILE_TYPE -- "Image" --> PIL
        SQLITE --> DATA_READY
        PIL --> DATA_READY
    end

    %% ── USER CHAT BLOCK ─────────────────────────────────────────
    subgraph CHAT ["💬 Chat Interface"]
        direction TB
        CHAT_UI[Chat UI — GET /chat\nchat.html]
        SEND_MSG["User types query\nPOST /chat\n{message: '...'}"]
        CHAT_UI --> SEND_MSG
    end

    %% ── AI ENGINE BLOCK ─────────────────────────────────────────
    subgraph AI ["🤖 AI Engine — query_csv_data_sql()"]
        direction TB

        HAS_DATA{Data\nloaded?}
        NO_DATA["⚠️ Return:\n'No data uploaded.\nAsk admin to upload.'"]

        INTENT["Intent Classifier\nScan STRATEGIC_KEYWORDS:\n'should','improve','recommend',\n'strategy','gap','beat'…"]
        QUERY_TYPE{Query\ntype?}

        subgraph SQL_PIPE ["📊 Text-to-SQL Pipeline"]
            direction TB
            SQL1["STEP 1 — SQL Generation\ngemini.ask_simple(schema + query)\n→ Raw SQL string"]
            SANITIZE["sanitize_sql()\nStrip markdown fences\nEnforce SELECT-only"]
            SAFE{SELECT\nonly?}
            UNSAFE["⚠️ Reject:\n'Unsafe query.\nRephrase'"]
            SQL2["STEP 2 — SQL Execution\nsqlite_conn.execute(sql)\ncursor.fetchmany(200)"]
            ROWS{Rows\nreturned?}
            NO_ROWS["⚠️ Return:\n'No results found.\nTry rephrasing.'"]
            IS_STRAT{is_strategic?}

            SQL1 --> SANITIZE --> SAFE
            SAFE -- NO --> UNSAFE
            SAFE -- YES --> SQL2
            SQL2 -- Exception --> ERR_HANDLER
            SQL2 --> ROWS
            ROWS -- NO --> NO_ROWS
            ROWS -- YES --> IS_STRAT
        end

        subgraph ANSWERS ["✍️ Answer Synthesis — Gemini Step 3"]
            direction LR
            STRATEGIC["STEP 3A — Strategic\nSystem: 'Senior CI Strategist'\nSections:\n• DATA SUMMARY\n• GAP / PROBLEM\n• RECOMMENDATIONS\n• EXPECTED IMPACT\n• NEXT STEPS"]
            ANALYTICAL["STEP 3B — Analytical\nSystem: 'CI Analyst'\nSections:\n• SUMMARY\n• KEY INSIGHTS\n• RECOMMENDATIONS"]
        end

        IMG_PATH["Image Path\nget_image_analysis()\nBuild img_context\n→ gemini.ask_simple()"]

        ERR_HANDLER["⚠️ Error Handler\n429 → Rate limit message\n403 → API key error\nOther → Generic error"]

        ASSEMBLE["Assemble result_parts[]\njoin with newlines\n→ JSON response"]

        HAS_DATA -- NO --> NO_DATA
        HAS_DATA -- YES --> INTENT
        INTENT --> QUERY_TYPE
        QUERY_TYPE -- Tabular --> SQL1
        QUERY_TYPE -- Image --> IMG_PATH

        IS_STRAT -- YES --> STRATEGIC
        IS_STRAT -- NO --> ANALYTICAL

        STRATEGIC --> ASSEMBLE
        ANALYTICAL --> ASSEMBLE
        IMG_PATH --> ASSEMBLE
        UNSAFE -.->|error path| ASSEMBLE
        NO_ROWS -.->|error path| ASSEMBLE
        ERR_HANDLER -.->|error path| ASSEMBLE
    end

    %% ── RESPONSE & EXIT ─────────────────────────────────────────
    RENDER["Render response in chat.html\n(plain-text labels, dash bullets)"]
    LOGOUT["GET /logout\nsession.clear()"]
    END_NODE([🏁 Session Ended])

    SEND_MSG --> HAS_DATA
    ASSEMBLE --> RENDER
    NO_DATA -.->|error path| RENDER
    RENDER -- "Send another query" -.->|loop| SEND_MSG
    RENDER -- "Logout" --> LOGOUT
    LOGOUT --> END_NODE

    %% ── STYLES ──────────────────────────────────────────────────
    classDef userNode    fill:#DAE8FC,stroke:#1B3A5C,color:#1B3A5C,rx:8
    classDef authNode    fill:#E1D5E7,stroke:#6A0572,color:#4A0060
    classDef adminNode   fill:#D5E8D4,stroke:#0D6E6E,color:#055555
    classDef aiNode      fill:#FFF3E0,stroke:#B45309,color:#7C3800
    classDef errorNode   fill:#F8CECC,stroke:#AE4132,color:#7A1C0D
    classDef termNode    fill:#1B3A5C,color:#FFFFFF,stroke:#1B3A5C
    classDef decNode     fill:#FFE6CC,stroke:#D6730D,color:#7C3800

    class START,END_NODE termNode
    class CHAT_UI,SEND_MSG,RENDER userNode
    class CHECK_SESSION,CHECK_ROLE,LOGIN_PAGE,VALIDATE,CREDS_OK,SET_SESSION authNode
    class LOGIN_ERR,NO_DATA,UNSAFE,NO_ROWS,ERR_HANDLER errorNode
    class ADMIN_DASH,UPLOAD,FILE_TYPE,PARSE,SQLITE,PIL,DATA_READY adminNode
    class INTENT,QUERY_TYPE,SQL1,SANITIZE,SAFE,SQL2,ROWS,IS_STRAT,STRATEGIC,ANALYTICAL,IMG_PATH,ASSEMBLE aiNode
    class LOGOUT authNode
```
