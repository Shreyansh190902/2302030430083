# Connect your phone and computer (free Firebase, about 10 minutes)

Your tracker on your domain can sync between devices through **Firebase**, Google's free database service. The free "Spark" plan is far more than a daily tracker needs, and no card is required.

## 1. Create the project
1. Open **https://console.firebase.google.com** and sign in with your Google account.
2. **Create a project**, name it e.g. `road-to-1-lakh`. Turn **off** Google Analytics (not needed) → **Create project**.

## 2. Turn on email sign-in
1. Left menu → **Build → Authentication → Get started**.
2. **Sign-in method** → **Email/Password** → switch **Enable** on → **Save**.
3. **Settings** tab → **Authorized domains** → **Add domain** → type your website's domain (e.g. `mytracker.in`) → **Add**.

## 3. Create the database
1. Left menu → **Build → Firestore Database → Create database**.
2. Location: **asia-south1 (Mumbai)** → **Next** → **Start in production mode** → **Create**.
3. Open the **Rules** tab, replace everything with the rules below, then **Publish**:

```
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    match /users/{uid}/{document=**} {
      allow read, write: if request.auth != null && request.auth.uid == uid;
    }
  }
}
```

These rules mean only you, signed in, can read or write your days. Nobody else can, even with your website address.

## 4. Get your web config
1. Click the ⚙️ gear (top left) → **Project settings** → scroll to **Your apps** → click the **`</>`** (Web) icon.
2. App nickname: `tracker` → **Register app** (skip Firebase Hosting).
3. Copy the whole `const firebaseConfig = { … };` block. It looks like:

```
const firebaseConfig = {
  apiKey: "AIza…",
  authDomain: "road-to-1-lakh.firebaseapp.com",
  projectId: "road-to-1-lakh",
  storageBucket: "road-to-1-lakh.appspot.com",
  messagingSenderId: "…",
  appId: "1:…:web:…"
};
```

This config is **not a password**. It only says which project to use; your rules and sign-in protect the data. You can paste it into the page, or send it to me and I'll build it into your `index.html` so you don't have to paste it on each device.

## 5. Connect each device
On your **computer** first (it has the most days, if any):
1. Open your website → **More** → **Cloud sync**.
2. Paste the config → **Connect**.
3. Type your email and a password (6+ characters) → **Create account**.

Then on your **iPhone**:
1. Open your website → **More** → **Cloud sync** → paste the same config → **Connect**.
2. Same email and password → **Sign in**.
3. If the phone already had days, it asks what to keep. **Combine both** keeps everything.

The badge at the top says **Synced** when it's working. Days you log on one device show up on the other within seconds. Offline days upload when you're back online.

## Troubleshooting
- **"Add this website's domain…"**: do step 2.3 (Authorized domains).
- **"Turn on Email/Password…"**: do step 2.2.
- **"Firebase refused access…"**: the Rules in step 3.3 weren't published.
- **Forgot password**: type your email → **Forgot password**. Firebase emails you a reset link.
