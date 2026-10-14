# Privacy

This is a self-hosted personal finance tracker. I (the developer) do not
run a server, and I never receive, store, or have access to anyone's
financial data. Each person runs their own copy of this software with
their own database and their own API credentials.

**What the app accesses**
When you connect an account, the app reads read-only account information
(account details, balances and transactions) from your bank or investment
provider. It does not make payments or move money.

**Where your data goes**

- Your data is requested directly from your provider's API (Monzo,
  Trading 212, or Enable Banking for banks that don't offer their own API)
  and stored in the PostgreSQL database that you set up and control.
- Your data is not sent to me or to any other third party, and the app
  contains no analytics, advertising or tracking.
- If you use Enable Banking to connect a bank, that data passes through
  Enable Banking's service under their own terms and privacy policy.

**What is stored**
Transactions, account names and numbers, and the access tokens needed to
keep your connections working. Access and refresh tokens are encrypted
before being saved. Your encryption key and API credentials are kept in
your own environment variables and are never committed to this repository.

**Your control**
You can stop the app at any time, revoke its access from your bank's or
provider's settings, and delete all stored data by deleting your database.

**Security**
You are responsible for securing your own machine and database. See the
"Security notes" section for recommendations.

**Contact**
Questions or concerns: open an issue at
https://github.com/guanyiwanggyw/Personal-Finance-Tracker/issues
