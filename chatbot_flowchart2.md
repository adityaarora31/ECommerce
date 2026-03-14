# Competitive Intelligence Chatbot — System Flowchart

```mermaid
flowchart TD

    START([START: User visits app]) --> CHECK_SESSION

    subgraph AUTH [Authentication Layer]
        direction TB
        CHECK_SESSION{Active session?}
        CHECK_ROLE{Role = Admin?}
        LOGIN_PAGE[Render login page]
        VALIDATE[check_password_hash\nVerify against users.json]
        CREDS_OK{Credentials valid?}
        SET_SESSION[Set session cookie\nusername and role]
        LOGIN_ERR[ERROR: Invalid credentials\nRe-render login page]

        CHECK_SESSION -->|NO| LOGIN_PAGE
        LOGIN_PAGE --> VALIDATE
        VALIDATE --> CREDS_OK
        CREDS_OK -->|NO| LOGIN_ERR
        LOGIN_ERR -.->|retry| LOGIN_PAGE
        CREDS_OK -->|YES| SET_SESSION
        SET_SESSION --> CHECK_ROLE
        CHECK_SESSION -->|YES| CHECK_ROLE
    end

    CHECK_ROLE -->|User| CHAT_UI
    CHECK_ROLE -->|Admin| ADMIN_DASH

    subgraph ADMIN [Admin Data Pipeline]
        direction TB
        ADMIN_DASH[Admin Dashboard - GET /admin]
        UPLOAD[Upload file\nPOST /admin/upload/type]
        FILE_TYPE{File type?}

        subgraph TABULAR [Tabular Data]
            PARSE[pandas read_csv / read_excel / json.load\nReturns DataFrame]
            SQLITE[make_table_name\nload_df_into_sqlite\nIn-memory SQLite DB]
            PARSE --> SQLITE
        end

        subgraph IMAGE_PIPE [Image Data]
            PIL[PIL Image.open\nanalyze_image\nStored in image_text_cache]
        end

        DATA_READY[(Data ready in memory\nsqlite_tables populated)]

        ADMIN_DASH --> UPLOAD
        UPLOAD --> FILE_TYPE
        FILE_TYPE -->|CSV / Excel / JSON| PARSE
        FILE_TYPE -->|Image| PIL
        SQLITE --> DATA_READY
        PIL --> DATA_READY
    end

    subgraph CHAT [Chat Interface]
        direction TB
        CHAT_UI[Chat UI - GET /chat]
        SEND_MSG[User sends query\nPOST /chat]
        CHAT_UI --> SEND_MSG
    end

    subgraph AI [AI Engine - query_csv_data_sql]
        direction TB

        HAS_DATA{Data loaded?}
        NO_DATA[ERROR: No data uploaded\nAsk admin to upload files]

        INTENT[Intent Classifier\nScan STRATEGIC_KEYWORDS\nshould, improve, recommend\nstrategy, gap, beat, outperform]
        QUERY_TYPE{Query type?}

        subgraph SQL_PIPE [Text-to-SQL Pipeline]
            direction TB
            SQL1[STEP 1 - SQL Generation\nGemini receives schema and query\nReturns raw SQL string]
            SANITIZE[sanitize_sql\nStrip markdown fences\nEnforce SELECT-only]
            SAFE{SELECT only?}
            UNSAFE[REJECTED: Unsafe query\nOnly SELECT statements allowed]
            SQL2[STEP 2 - SQL Execution\nsqlite_conn.execute sql\ncursor.fetchmany 200 rows]
            ROWS{Rows returned?}
            NO_ROWS[ERROR: No results\nTry rephrasing the query]
            IS_STRAT{is_strategic?}

            SQL1 --> SANITIZE --> SAFE
            SAFE -->|NO| UNSAFE
            SAFE -->|YES| SQL2
            SQL2 -->|Exception| ERR_HANDLER
            SQL2 --> ROWS
            ROWS -->|NO| NO_ROWS
            ROWS -->|YES| IS_STRAT
        end

        subgraph ANSWERS [Answer Synthesis - Gemini Step 3]
            direction LR
            STRATEGIC[STEP 3A - Strategic Answer\nRole: Senior CI Strategist\nSections: DATA SUMMARY\nGAP - RECOMMENDATIONS\nEXPECTED IMPACT - NEXT STEPS]
            ANALYTICAL[STEP 3B - Analytical Answer\nRole: CI Analyst\nSections: SUMMARY\nKEY INSIGHTS - RECOMMENDATIONS]
        end

        IMG_PATH[Image Path\nget_image_analysis\nGemini ask_simple]
        ERR_HANDLER[ERROR Handler\n429: Rate limit exceeded\n403: API key error\nOther: Generic error message]
        ASSEMBLE[Assemble result_parts\nJoin with newlines\nReturn JSON response]

        HAS_DATA -->|NO| NO_DATA
        HAS_DATA -->|YES| INTENT
        INTENT --> QUERY_TYPE
        QUERY_TYPE -->|Tabular| SQL1
        QUERY_TYPE -->|Image| IMG_PATH

        IS_STRAT -->|YES| STRATEGIC
        IS_STRAT -->|NO| ANALYTICAL

        STRATEGIC --> ASSEMBLE
        ANALYTICAL --> ASSEMBLE
        IMG_PATH --> ASSEMBLE
        UNSAFE -.-> ASSEMBLE
        NO_ROWS -.-> ASSEMBLE
        ERR_HANDLER -.-> ASSEMBLE
    end

    RENDER[Render response in chat.html]
    LOGOUT[GET /logout\nsession.clear]
    END_NODE([END: Session Ended])

    SEND_MSG --> HAS_DATA
    ASSEMBLE --> RENDER
    NO_DATA -.-> RENDER
    RENDER -.->|Send another query| SEND_MSG
    RENDER -->|Logout| LOGOUT
    LOGOUT --> END_NODE

    classDef userNode  fill:#DAE8FC,stroke:#1B3A5C,color:#1B3A5C
    classDef authNode  fill:#E1D5E7,stroke:#6A0572,color:#4A0060
    classDef adminNode fill:#D5E8D4,stroke:#0D6E6E,color:#055555
    classDef aiNode    fill:#FFF3E0,stroke:#B45309,color:#7C3800
    classDef errorNode fill:#F8CECC,stroke:#AE4132,color:#7A1C0D
    classDef termNode  fill:#1B3A5C,color:#FFFFFF,stroke:#1B3A5C

    class START,END_NODE termNode
    class CHAT_UI,SEND_MSG,RENDER userNode
    class CHECK_SESSION,CHECK_ROLE,LOGIN_PAGE,VALIDATE,CREDS_OK,SET_SESSION,LOGOUT authNode
    class LOGIN_ERR,NO_DATA,UNSAFE,NO_ROWS,ERR_HANDLER errorNode
    class ADMIN_DASH,UPLOAD,FILE_TYPE,PARSE,SQLITE,PIL,DATA_READY adminNode
    class INTENT,QUERY_TYPE,SQL1,SANITIZE,SAFE,SQL2,ROWS,IS_STRAT,STRATEGIC,ANALYTICAL,IMG_PATH,ASSEMBLE aiNode
```
