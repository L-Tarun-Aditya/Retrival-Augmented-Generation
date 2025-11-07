# RAG Chat Frontend

Modern chat interface for the RAG (Retrieval-Augmented Generation) system built with Next.js 14 and shadcn/ui.

## Features

- 💬 Real-time chat interface
- 🎨 Beautiful UI with shadcn/ui components
- 📱 Responsive design
- 🔍 View retrieved context for each answer
- ⚡ Fast and smooth interactions
- 🌙 Dark mode support (via Tailwind)

## Tech Stack

- **Next.js 14** - React framework with App Router
- **TypeScript** - Type safety
- **Tailwind CSS** - Styling
- **shadcn/ui** - UI components
- **Lucide React** - Icons

## Getting Started

### Install Dependencies
```bash
npm install
```

### Run Development Server
```bash
npm run dev
```

Open [http://localhost:3000](http://localhost:3000)

### Build for Production
```bash
npm run build
npm start
```

## Configuration

The frontend expects the API to be running on `http://localhost:8000`. To change this, update the fetch URL in `components/chat.tsx`.

## Components

- `components/chat.tsx` - Main chat interface
- `components/ui/*` - shadcn/ui components (Button, Card, Input, ScrollArea)
- `lib/utils.ts` - Utility functions

## Customization

### Colors
Edit `app/globals.css` to customize the color scheme.

### API Endpoint
Update the fetch URL in `components/chat.tsx`:
```typescript
const response = await fetch("YOUR_API_URL/query", {
  // ...
})
```

## License

MIT
