# capstoneProject
## Motivation 
The proposed Customer Activation and Engagement Prediction Project would add significant value to STADIOEquities because it addresses one of the company’s most important commercial challenges: converting registered users into funded, active and long-term investors. Although STADIOEquities has successfully attracted approximately 2.3 million registered accounts, only about 760,000 are currently funded and active, while 41% of registered accounts have never made a deposit. The briefing pack further states that the company spends approximately R180 to acquire each account, and this acquisition cost is only recovered when the account becomes active. This means that attracting more registrations on its own does not necessarily create value; value is generated when clients fund their accounts and continue using the platform.

The project is particularly relevant to the company’s current state because STADIOEquities is experiencing a weakening customer activation and retention funnel. The conversion rate from sign-up to first deposit has fallen from 64% to 59%, while the proportion of accounts becoming dormant within six months has increased from 22% to 31%. KYC abandonment has also increased from 13% to 18%. At present, onboarding emails and nudges are sent according to the same fixed schedule to all customers, even though the briefing pack explains that customer drop-off is not random and is associated with factors such as acquisition channel, onboarding progress, first-session behaviour and the time taken to make a first deposit. A predictive solution could therefore use these behavioural signals to identify customers who are likely to activate, customers at risk of abandoning onboarding, and customers who may become dormant, allowing STADIOEquities to intervene at a more appropriate time.

Improving activation and engagement would also have a direct financial benefit because almost every major STADIOEquities revenue stream depends on clients funding and using their accounts. Platform and administration fees contribute 38% of revenue, brokerage and transaction fees contribute 29%, interest on uninvested cash contributes 17%, premium subscriptions contribute 10%, and value-added products contribute a further 6%. The briefing pack specifically notes that growing client balances and maintaining engagement are fundamental to the company’s economics. Increasing the number of customers who make their first deposit and remain active could therefore increase assets under administration, trading activity and opportunities for appropriate premium and value-added product adoption.

The project is also feasible because STADIOEquities already possesses the data required to build such a solution. The company records app and web behaviour, onboarding activity, funding information, transactions, product subscriptions, customer demographics, support interactions and marketing engagement across several years. A unified client-data platform is already being developed to bring these behavioural, financial and service datasets together. This creates a strong foundation for using data analytics or machine-learning techniques to identify patterns associated with successful activation and future inactivity.

Most importantly, the project directly supports STADIOEquities' 2030 Strategy. Two of the strategy's stated priorities are to activate existing accounts by identifying who is likely to activate or stall and intervening at the right moment, and to keep clients engaged by detecting dormancy before an account becomes inactive. The proposed project therefore responds to a current, measurable business problem while supporting the organisation's longer-term goal of transforming its large registration base into a durable and valuable client base. Rather than simply acquiring more customers, STADIOEquities would be able to make better use of customers it has already acquired, reduce wasted marketing expenditure, improve customer engagement and strengthen sustainable revenue growth.

## Problem Statement

STADIOEquities has successfully attracted approximately 2.3 million registered customers, yet a large proportion of these customers do not progress into funded and active investors. Around 41% of registered accounts have never made a deposit, while the sign-up-to-first-deposit conversion rate has declined from 64% to 59%. In addition, the percentage of accounts becoming dormant within six months has increased from 22% to 31%, indicating that STADIOEquities is not only struggling to activate new customers but also to retain their engagement after registration.

A key challenge is that STADIOEquities currently sends onboarding communication and nudges to customers on a fixed schedule, despite having data showing that customer drop-off is associated with factors such as acquisition channel, onboarding progress, first-session behaviour and the time taken to make a first deposit. The company therefore lacks an effective way of identifying which customers are likely to fund their accounts, which are likely to abandon the onboarding process, and which active customers are at risk of becoming dormant.

The Data Science problem is therefore to use STADIOEquities' historical behavioural, onboarding, funding, trading, demographic and marketing data to develop a predictive model that can identify customers who are at high risk of failing to activate or becoming dormant. The resulting predictions could enable STADIOEquities to target interventions and customer engagement efforts more effectively, rather than treating all customers in the same way. This is well suited to a Data Science project because STADIOEquities already holds several years of customer behavioural and financial data that can be analysed to uncover patterns and develop predictive models.


## 1. Client and Account Data

STADIOEquities has approximately **2.3 million registered accounts**, with only a portion funded and active. This dataset therefore provides the base population for the project.

| Column name | Data type | Example | Additional information |
|---|---|---|---|
| `Client ID` | String, identifier | `C102938` | Unique anonymised identifier for each client. Must remain consistent across all datasets. |
| `Account ID` | String, identifier | `A458921` | Unique investment account identifier. |
| `Registration date` | Datetime | `2025-03-14 10:26:13` | Date and time the account was created. Use `yyyy-MM-dd hh:mm:ss`. |
| `Account status` | String, categorical | `Active` | Valid values should include `Registered`, `Active`, `Dormant`, `Closed`, or equivalent internal categories. |
| `Activation date` | Datetime | `2025-03-17 14:05:00` | Date the customer first met STADIOEquities' definition of an activated account. Null if never activated. |
| `First deposit date` | Datetime | `2025-03-17 13:42:00` | Date and time of first successful deposit. Null for never-funded clients. |
| `Account closure date` | Datetime | `2026-01-20 09:00:00` | Null if the account remains open. |
| `KYC status` | String, categorical | `Complete` | Examples: `Not Started`, `In Progress`, `Complete`, `Failed`. |
| `KYC completion date` | Datetime | `2025-03-14 10:48:00` | Null if KYC was not completed. |
| `Age` | Numeric, integer | `31` | Age at registration, or date of birth transformed into age. |
| `Province/region` | String, categorical | `GP` | Region or province recorded at registration. |
| `Stated investment goal` | String, categorical | `Long-term growth` | Preserve the categories currently captured at sign-up. |
| `Risk appetite` | String, categorical | `Moderate` | Use the actual categories used by STADIOEquities, e.g. `Low`, `Moderate`, `High`. |
| `Client segment` | String, categorical | `Retail` | If an internal customer segment already exists, provide it. Do not create one specifically for this extract. |
| `Acquisition channel` | String, categorical | `Paid Social` | Channel through which the client was acquired. |
| `Acquisition campaign` | String | `InvestStart2025` | Campaign identifier or campaign name. |
| `Acquisition cost` | Numeric, decimal | `180.00` | Cost attributable to acquiring the account, in rand. |
| `Latest activity date` | Datetime | `2026-08-27 18:45:20` | Most recent qualifying account activity. |
| `Days since last activity` | Numeric, integer | `10` | Ideally derive from raw activity dates, while also providing the current field if available. |
| `Funded flag` | Boolean | `TRUE` | `TRUE` if the account has ever received a successful deposit. |
| `Active flag` | Boolean | `TRUE` | Use STADIOEquities' official business definition of active. The briefing refers to active accounts as traded or held in the last 90 days. |
| `Dormant flag` | Boolean | `FALSE` | Supply the current internal dormancy classification and its business definition. |

---

## 2. Onboarding and KYC Journey Data

This dataset is particularly important because KYC abandonment has increased, and the briefing indicates that **where a customer drops out during onboarding is associated with whether they eventually activate**.

**Grain:** one row per onboarding/KYC event.

| Column name | Data type | Example | Additional information |
|---|---|---|---|
| `Client ID` | String, identifier | `C102938` | Must link to the client table. |
| `Account ID` | String, identifier | `A458921` | Must link to the account table. |
| `Onboarding session ID` | String | `S849222` | Unique onboarding session identifier. |
| `Step name` | String, categorical | `Identity Verification` | Name of onboarding/KYC step. |
| `Step number` | Numeric, integer | `4` | Sequential position within onboarding journey. |
| `Step start time` | Datetime | `2025-03-14 10:31:20` | When the customer entered the step. |
| `Step completion time` | Datetime | `2025-03-14 10:33:44` | Null if the step was abandoned. |
| `Step completed` | Boolean | `TRUE` | `TRUE` if successfully completed. |
| `Abandoned flag` | Boolean | `FALSE` | `TRUE` where the customer left before completion. |
| `Abandonment reason` | String, categorical | `Document upload failed` | Provide where recorded. |
| `Error code` | String | `KYC203` | System error encountered during onboarding. |
| `Retry count` | Numeric, integer | `2` | Number of attempts at the particular step. |
| `Time on step` | Numeric, decimal | `144` | Preferably measured in seconds. |
| `Device type` | String, categorical | `Mobile` | Examples: `Mobile`, `Desktop`, `Tablet`. |
| `Platform` | String, categorical | `Android` | Examples: `Android`, `iOS`, `Web`. |
| `App version` | String | `9.4.1` | Useful for identifying technical friction associated with particular releases. |
| `Referral source` | String, categorical | `Instagram` | Source immediately before onboarding, where available. |

---

## 3. App and Web Behaviour Data

The briefing states that STADIOEquities records screens viewed, sessions, feature usage, onboarding steps, and abandonment, with approximately **four years of history**. This is likely to be one of the most important datasets for predicting both activation and future dormancy.

**Grain:** one row per app/web event.

| Column name | Data type | Example | Additional information |
|---|---|---|---|
| `Client ID` | String, identifier | `C102938` | Anonymised customer identifier. |
| `Session ID` | String | `S938102` | Unique browsing/app session. |
| `Event ID` | String | `E298374` | Unique event identifier. |
| `Event datetime` | Datetime | `2025-03-14 10:20:14` | Exact event timestamp. |
| `Event type` | String, categorical | `Screen View` | Examples: `Screen View`, `Button Click`, `Search`, `Login`, `Logout`, `Error`. |
| `Screen name` | String, categorical | `Deposit` | Name of screen viewed. |
| `Feature name` | String, categorical | `Deposit Funds` | Feature being used. |
| `Action` | String, categorical | `Click` | User action associated with the event. |
| `Session start` | Datetime | `2025-03-14 10:18:02` | Beginning of customer session. |
| `Session end` | Datetime | `2025-03-14 10:41:18` | End of session. |
| `Session duration` | Numeric, integer | `1396` | Duration in seconds. |
| `Screens viewed` | Numeric, integer | `12` | Can be provided as a derived session-level measure in addition to raw events. |
| `Device type` | String, categorical | `Smartphone` | Device category. |
| `Operating system` | String, categorical | `Android` | Examples: `Android`, `iOS`, `Windows`, `macOS`, etc. |
| `App/Web` | String, categorical | `App` | `App` or `Web`. |
| `Login status` | String, categorical | `Authenticated` | Indicates whether the customer was logged in. |
| `Error encountered` | Boolean | `FALSE` | Indicates whether a technical error occurred. |
| `Error code` | String | `DEP001` | Null when there was no error. |
| `Search term` | String | `how to deposit` | Where search functionality is available; sensitive/free-text fields should be appropriately governed. |
| `Days since registration` | Numeric, integer | `0` | Ideally derived during modelling rather than replacing the raw dates. |
| `Days since previous session` | Numeric, integer | `3` | Can be derived from timestamp history. |

> **Data granularity note:** Please provide raw event-level data where possible, rather than only summary statistics. Raw records allow alternative measures to be constructed during modelling if necessary.

---

## 4. Deposits, Withdrawals and Funding Data

This dataset is essential because the project's first target is whether a registered client progresses to a funded account. The briefing provides up to **six years of account and funding history**, including deposits, withdrawals, and balances.

**Grain:** one row per financial movement.

| Column name | Data type | Example | Additional information |
|---|---|---|---|
| `Client ID` | String, identifier | `C102938` | Must correspond with other datasets. |
| `Account ID` | String, identifier | `A458921` | Investment account involved. |
| `Transaction ID` | String | `TX2039485` | Unique transaction identifier. |
| `Transaction datetime` | Datetime | `2025-03-17 13:42:00` | Exact date/time the transaction occurred. |
| `Transaction type` | String, categorical | `Deposit` | Examples: `Deposit`, `Withdrawal`, `Transfer`. |
| `Transaction status` | String, categorical | `Successful` | Examples: `Successful`, `Pending`, `Failed`, `Reversed`. |
| `Amount` | Numeric, decimal | `500.00` | Transaction amount in rand. |
| `Balance before` | Numeric, decimal | `0.00` | Account cash balance before transaction. |
| `Balance after` | Numeric, decimal | `500.00` | Account cash balance after transaction. |
| `Deposit method` | String, categorical | `EFT` | Payment/funding mechanism. |
| `Deposit sequence` | Numeric, integer | `1` | `1` indicates first deposit, `2` second deposit, etc. |
| `Failure reason` | String, categorical | `Bank declined` | Required for failed deposits where available. |
| `Days since registration` | Numeric, integer | `3` | Time between account creation and this funding event. |
| `First deposit flag` | Boolean | `TRUE` | `TRUE` for the first successful deposit. |

---

## 5. Trading and Portfolio Activity

The briefing states that STADIOEquities has around **six years of data** covering trades, instruments held, trading frequency, concentration, and timing. For the dormancy model, changes in trading behaviour may provide strong early-warning signals.

**Grain:** one row per trade.

| Column name | Data type | Example | Additional information |
|---|---|---|---|
| `Client ID` | String, identifier | `C102938` | Customer identifier. |
| `Account ID` | String, identifier | `A458921` | Investment account. |
| `Trade ID` | String | `T398483` | Unique trade identifier. |
| `Trade datetime` | Datetime | `2025-04-03 11:34:25` | Exact trade timestamp. |
| `Trade type` | String, categorical | `Buy` | `Buy` or `Sell`. |
| `Instrument ID` | String | `STX40` | Instrument identifier/ticker. |
| `Instrument type` | String, categorical | `ETF` | Examples: `Share`, `ETF`, `Bundle`, `Offshore asset`. |
| `Quantity` | Numeric, decimal | `2.5` | Fractional shares should be preserved. |
| `Trade value` | Numeric, decimal | `450.00` | Total rand value of transaction. |
| `Fees` | Numeric, decimal | `4.50` | Total fees charged. |
| `Portfolio value` | Numeric, decimal | `6200.00` | Portfolio value at or near trade date, if available. |
| `Cash balance` | Numeric, decimal | `850.00` | Uninvested cash balance. |
| `Number holdings` | Numeric, integer | `6` | Number of instruments held at that point in time. |
| `Largest holding %` | Numeric, decimal | `42.5` | Percentage of portfolio represented by the largest position. |
| `Days since previous trade` | Numeric, integer | `28` | Useful signal for declining engagement. |
| `Trade sequence` | Numeric, integer | `7` | Customer's nth transaction. |

---

## 6. Marketing, Emails and Customer Nudges

This dataset is important because the current approach sends onboarding emails and nudges on a fixed schedule, regardless of individual customer behaviour. The model should be able to assess how communication exposure and engagement relate to activation.

**Grain:** one row per marketing/customer communication event.

| Column name | Data type | Example | Additional information |
|---|---|---|---|
| `Client ID` | String, identifier | `C102938` | Must link across data sources. |
| `Communication ID` | String | `COM58302` | Unique email/SMS/push/nudge identifier. |
| `Campaign ID` | String | `ONB2025A` | Marketing/onboarding campaign. |
| `Communication type` | String, categorical | `Push Notification` | Examples: `Email`, `SMS`, `Push`, `In-app`. |
| `Message category` | String, categorical | `First Deposit Reminder` | Business purpose of communication. |
| `Sent datetime` | Datetime | `2025-03-16 09:00:00` | Time communication was sent. |
| `Delivered` | Boolean | `TRUE` | Delivery status. |
| `Opened` | Boolean | `TRUE` | Whether opened/viewed. |
| `Open datetime` | Datetime | `2025-03-16 09:12:10` | Null if not opened. |
| `Clicked` | Boolean | `TRUE` | Whether the customer clicked through. |
| `Click datetime` | Datetime | `2025-03-16 09:13:05` | Null if no click. |
| `Converted` | Boolean | `TRUE` | Whether the intended action followed, if STADIOEquities currently calculates this. |
| `Conversion datetime` | Datetime | `2025-03-17 13:42:00` | Time of conversion. |
| `Days after registration` | Numeric, integer | `2` | Communication timing relative to sign-up. |
| `Opt-out flag` | Boolean | `FALSE` | Whether the customer has opted out of that communication channel. |

The briefing confirms that marketing data includes acquisition channel, campaign, cost, and email/nudge engagement, with approximately **four years of history**.

---

## 7. Product and Subscription Data

Although premium adoption is not the primary target, product usage provides information about the depth of customer engagement. The briefing notes that premium take-up has declined from **4.6% to 4.1%**, and that the premium offering is currently marketed generically across a diverse customer base.

**Grain:** one row per product/subscription event.

| Column name | Data type | Example | Additional information |
|---|---|---|---|
| `Client ID` | String, identifier | `C102938` | Customer identifier. |
| `Account ID` | String, identifier | `A458921` | Investment account. |
| `Product ID` | String | `P004` | Product identifier. |
| `Product type` | String, categorical | `Tax-Free Account` | Product/category name. |
| `Subscription tier` | String, categorical | `Premium` | Current or historical subscription level. |
| `Start date` | Date | `2025-06-01` | Date product/subscription started. |
| `Cancellation date` | Date | `2026-01-10` | Null if still active. |
| `Subscription status` | String, categorical | `Active` | Examples: `Active`, `Cancelled`, `Expired`, `Trial`, etc. |
| `Monthly fee` | Numeric, decimal | `49.00` | Fee in rand where applicable. |
| `Cancellation reason` | String, categorical | `Low usage` | Provide if captured. |
| `Product usage count` | Numeric, integer | `7` | Number of interactions with the product over an agreed time window, if already available. |

---

## 8. Client Service and Support Data

Support volumes have increased from **46 to 63 tickets per 1,000 active clients**, and the briefing notes that free-text customer queries are not currently mined systematically. Support activity may therefore reveal frustration or disengagement before dormancy occurs.

**Grain:** one row per ticket or interaction.

| Column name | Data type | Example | Additional information |
|---|---|---|---|
| `Client ID` | String, identifier | `C102938` | Customer identifier. |
| `Ticket ID` | String | `SUP39483` | Unique support interaction. |
| `Created datetime` | Datetime | `2026-05-13 09:15:23` | Ticket creation time. |
| `Closed datetime` | Datetime | `2026-05-13 14:05:10` | Null if unresolved. |
| `Contact channel` | String, categorical | `In-app chat` | Examples: `Email`, `Chat`, `Phone`, `Web`. |
| `Ticket category` | String, categorical | `Withdrawal` | Existing classification. |
| `Ticket subcategory` | String, categorical | `Withdrawal delayed` | More detailed categorisation, if available. |
| `Query text` | String, free text | `Why can't I withdraw?` | Please provide de-identified text. The briefing specifically identifies free-text support queries as an available source. |
| `Resolution status` | String, categorical | `Resolved` | Examples: `Open`, `Resolved`, `Escalated`, etc. |
| `Resolution time` | Numeric, integer | `290` | Minutes to resolution. |
| `Escalated` | Boolean | `FALSE` | Whether the ticket required escalation. |
| `Repeat contact flag` | Boolean | `TRUE` | Whether the client contacted support repeatedly for the same issue, if available. |
| `Satisfaction score` | Numeric | `3` | Provide the existing scale, e.g. `1–5`. |
| `Complaint flag` | Boolean | `FALSE` | `TRUE` where the interaction became a formal complaint. |

---

## 9. Outcome / Target Data

This table is essential because the machine-learning models require historical examples of customers who **did and did not activate**, as well as those who **did and did not become dormant**.

| Column name | Data type | Example | Additional information |
|---|---|---|---|
| `Client ID` | String, identifier | `C102938` | Links the outcome to predictor data. |
| `Registration date` | Date | `2025-03-14` | Required for defining the activation observation window. |
| `Ever funded` | Boolean | `TRUE` | `TRUE` if the client has ever successfully deposited. |
| `First deposit date` | Datetime | `2025-03-17 13:42:00` | Null for never-funded accounts. |
| `Activation outcome` | Boolean | `TRUE` | Final modelling label. Definition should be agreed with STADIOEquities before modelling. |
| `Days to activation` | Numeric, integer | `3` | Days from registration to first successful activation event. |
| `Dormancy date` | Date | `2026-02-10` | Date the client met the official dormancy definition. |
| `Dormancy outcome` | Boolean | `TRUE` | Historical target for dormancy prediction. |
| `Reactivation date` | Date | `2026-05-20` | Useful for distinguishing temporary dormancy from permanent disengagement. |
| `Reactivated flag` | Boolean | `TRUE` | `TRUE` if the customer later became active again. |
| `Account closed` | Boolean | `FALSE` | Separate closure from dormancy. |

---

## Important Definitions to Confirm Before Modelling

Before modelling begins, STADIOEquities should confirm the exact operational definitions of the following terms.

### Activation

For example, clarify whether a customer becomes activated:

- immediately after their **first successful deposit**; or
- only after **funding and completing a trade**.

### Dormancy

The briefing reports accounts that become dormant within six months and describes funded and active accounts as having **"traded or held in the last 90 days"**, but it does not provide a complete formal modelling definition of dormancy.

The following should therefore be agreed before creating the target variable:

- the exact number of inactive days required for dormancy;
- which customer actions count as qualifying activity; and
- how temporary dormancy, reactivation, and permanent disengagement should be treated.

---

## Data Delivery Requirements

The maximum historical data available should be requested, rather than only the most recent customers.

According to the briefing, STADIOEquities has approximately:

| Data source | Historical coverage |
|---|---:|
| App/web data | 4 years |
| Account and funding data | 6 years |
| Trading activity | 6 years |
| Product/subscription data | 4 years |
| Demographics | 6 years |
| Support data | 3 years |
| Marketing data | 4 years |

### General delivery standards

The client should provide the data at the **lowest practical level of detail**, preferably event- or transaction-level rather than only monthly totals.

All supplied datasets should meet the following requirements:

- Use a consistent, anonymised `Client ID` across all relevant tables.
- Include `Account ID` where account-level relationships are required.
- Prefer timestamps in `yyyy-MM-dd hh:mm:ss` format.
- Keep missing values identifiable rather than silently replacing them with zero.
- Supply categorical codes together with a supporting data dictionary.
- Preserve raw event and transaction timestamps where available.
- Exclude unnecessary personally identifying information such as:
  - names;
  - identity numbers;
  - phone numbers; and
  - email addresses.
- De-identify free-text fields before delivery where necessary.

---

## Intended Customer Journey View

Together, these datasets would allow the project to construct a chronological view of each client's journey:

```text
Registration
    ↓
Onboarding / KYC
    ↓
First Deposit
    ↓
Initial Investment Activity
    ↓
Ongoing Engagement
    ↓
Active / Dormant / Reactivated / Closed
```

This combined view would support predictive models that directly address STADIOEquities' **activation** and **engagement/dormancy** problem.

| **RAAIDD**                                                                                     | **Description**                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |
| ---------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Risk 1 – Incomplete linking of customer data**                                               | STADIOEquities stores customer information across app/web behaviour, account funding, trading, marketing, product, support and demographic datasets. There is a risk that the same customer cannot be consistently linked across these sources because identity spans app and web sessions. This could prevent the project from building a complete customer journey and reduce the accuracy of the activation and dormancy models.                                                                         |
| **Risk 2 – Class imbalance in the prediction targets**                                         | The model may contain significantly more activated customers than non-activated customers, or more active customers than customers who become dormant. For example, 41% of registered accounts have never funded, while 31% of accounts become dormant within six months. If this imbalance is not addressed, a model could appear accurate while performing poorly at identifying the customers STADIOEquities actually needs to intervene with.                                                           |
| **Action 1 – Obtain and profile the required historical data**                                 | Request and assess the available customer-level and event-level data covering registration, onboarding/KYC, app and web activity, deposits, withdrawals, trading, marketing communications, product usage and support interactions. Initial profiling will check missing values, duplicates, inconsistent IDs, date ranges, class balance and whether all required variables are available before modelling begins.                                                                                         |
| **Action 2 – Build and evaluate prediction models**                                            | Create separate predictive models for **activation** and **dormancy**. The activation model will estimate the likelihood that a newly registered customer will make a first deposit, while the dormancy model will identify funded or active customers who are at risk of becoming inactive. The models will be compared using suitable evaluation measures such as precision, recall, F1-score, ROC-AUC and confusion matrices, with particular focus on correctly identifying high-risk customers.        |
| **Assumption 1 – Historical behaviour is predictive of future behaviour**                      | It is assumed that patterns such as onboarding completion, acquisition channel, first-session activity, deposit timing and recent platform usage have a meaningful relationship with future activation or dormancy. This assumption is reasonable because the briefing pack states that customer drop-off clusters according to how the customer arrived, onboarding progress, first-session behaviour and the time taken to make the first deposit.                                                        |
| **Assumption 2 – Sufficient historical data will be available**                                | It is assumed that STADIOEquities can provide enough historical observations to train and test the models. The briefing indicates that the company has between three and six years of historical data across behavioural, account, trading, marketing, product and support systems, which should provide sufficient observations if the datasets can be successfully joined.                                                                                                                                |
| **Issue – Activation and dormancy definitions are not yet sufficiently precise for modelling** | The briefing identifies funded/active accounts and reports accounts becoming dormant within six months, but it does not provide a complete modelling definition of when a customer should officially be labelled as “activated” or “dormant”. This must be resolved with STADIOEquities stakeholders before the target variables can be created. For example, activation could mean first successful deposit, while dormancy could be defined as no qualifying activity for an agreed number of days.       |
| **Decision – Develop two related predictive models rather than one general engagement model**  | The project will separately predict **failure to activate** and **risk of future dormancy**. These represent different stages of the customer lifecycle and require different intervention strategies. A newly registered customer who has never deposited should not be treated in the same way as an existing investor whose activity is declining. This decision also aligns directly with STADIOEquities' strategy to both increase account activation and detect dormancy before customers disengage.  |
| **Dependency 1 – Data access must be completed before model development**                      | Data extraction, anonymisation, integration and quality assessment must be completed before feature engineering and model training can begin. In particular, Client ID and Account ID must be consistently mapped across behavioural, funding, trading and marketing sources before a customer-level modelling dataset can be created.                                                                                                                                                                      |
| **Dependency 2 – Target definitions must be agreed before training data can be prepared**      | STADIOEquities stakeholders must approve the definitions and observation windows for **activation** and **dormancy** before customers can be labelled for supervised machine learning. Once these definitions are agreed, historical records can be labelled, features can be calculated using only information available before the prediction point, and model training and validation can proceed.                                                                                                       |

