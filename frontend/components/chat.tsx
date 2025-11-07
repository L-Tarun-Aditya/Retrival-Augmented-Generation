"use client"

import { useState, useRef } from "react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { ScrollArea } from "@/components/ui/scroll-area"
import { Send, Loader2, BookOpen, Bot, User, Upload, FileText, ChevronLeft, ChevronRight, RefreshCw } from "lucide-react"

interface Message {
  role: "user" | "assistant"
  content: string
  context?: string[]
}

interface Document {
  filename: string
  size: number
}

export default function Chat() {
  const [messages, setMessages] = useState<Message[]>([])
  const [input, setInput] = useState("")
  const [loading, setLoading] = useState(false)
  const [showContext, setShowContext] = useState(false)
  const [uploading, setUploading] = useState(false)
  const [uploadStatus, setUploadStatus] = useState("")
  const [uploadProgress, setUploadProgress] = useState(0)
  const [documents, setDocuments] = useState<Document[]>([])
  const [sidebarOpen, setSidebarOpen] = useState(true)
  const [loadingDocs, setLoadingDocs] = useState(false)
  const fileInputRef = useRef<HTMLInputElement>(null)

  const fetchDocuments = async () => {
    setLoadingDocs(true)
    try {
      const response = await fetch("http://localhost:8000/documents")
      if (response.ok) {
        const data = await response.json()
        setDocuments(data.documents || [])
      }
    } catch (error) {
      console.error("Error fetching documents:", error)
    } finally {
      setLoadingDocs(false)
    }
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!input.trim() || loading) return

    const userMessage: Message = { role: "user", content: input }
    setMessages((prev) => [...prev, userMessage])
    setInput("")
    setLoading(true)

    try {
      const response = await fetch("http://localhost:8000/query", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          question: input,
          n_results: 3,
        }),
      })

      if (!response.ok) {
        throw new Error("Failed to get response")
      }

      const data = await response.json()
      const assistantMessage: Message = {
        role: "assistant",
        content: data.answer,
        context: data.context,
      }

      setMessages((prev) => [...prev, assistantMessage])
    } catch (error) {
      console.error("Error:", error)
      const errorMessage: Message = {
        role: "assistant",
        content: "Sorry, I encountered an error. Please make sure the API server is running.",
      }
      setMessages((prev) => [...prev, errorMessage])
    } finally {
      setLoading(false)
    }
  }

  const handleFileUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0]
    if (!file) return

    if (!file.name.endsWith('.pdf')) {
      setUploadStatus("Error: Only PDF files are supported")
      setTimeout(() => setUploadStatus(""), 3000)
      return
    }

    setUploading(true)
    setUploadProgress(0)
    setUploadStatus(`Uploading ${file.name}...`)

    try {
      const formData = new FormData()
      formData.append("file", file)

      // Simulate progress stages
      const progressInterval = setInterval(() => {
        setUploadProgress((prev) => {
          if (prev >= 90) return prev
          return prev + 10
        })
      }, 200)

      const response = await fetch("http://localhost:8000/upload-document", {
        method: "POST",
        body: formData,
      })

      clearInterval(progressInterval)
      setUploadProgress(100)

      if (!response.ok) {
        throw new Error("Failed to upload document")
      }

      const data = await response.json()
      setUploadStatus(`✓ ${data.message}`)
      
      // Refresh document list
      fetchDocuments()
      
      // Clear status after 3 seconds
      setTimeout(() => {
        setUploadStatus("")
        setUploadProgress(0)
      }, 3000)
    } catch (error) {
      console.error("Upload error:", error)
      setUploadStatus("Error: Failed to upload document")
      setUploadProgress(0)
      setTimeout(() => setUploadStatus(""), 3000)
    } finally {
      setUploading(false)
      if (fileInputRef.current) {
        fileInputRef.current.value = ""
      }
    }
  }

  // Load documents on mount
  useState(() => {
    fetchDocuments()
  })

  const formatFileSize = (bytes: number) => {
    if (bytes < 1024) return bytes + " B"
    if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1) + " KB"
    return (bytes / (1024 * 1024)).toFixed(1) + " MB"
  }

  return (
    <div className="flex h-screen max-w-7xl mx-auto p-4 gap-4">
      {/* Sidebar */}
      <div className={`transition-all duration-300 ${sidebarOpen ? 'w-64' : 'w-0'} overflow-hidden`}>
        <Card className="h-full flex flex-col">
          <CardHeader className="pb-3">
            <div className="flex items-center justify-between">
              <CardTitle className="text-sm flex items-center gap-2">
                <FileText className="h-4 w-4" />
                Documents
              </CardTitle>
              <Button
                variant="ghost"
                size="sm"
                onClick={fetchDocuments}
                disabled={loadingDocs}
                className="h-7 w-7 p-0"
              >
                <RefreshCw className={`h-3 w-3 ${loadingDocs ? 'animate-spin' : ''}`} />
              </Button>
            </div>
          </CardHeader>
          <CardContent className="flex-1 overflow-hidden p-0">
            <ScrollArea className="h-full px-4 pb-4">
              {documents.length === 0 ? (
                <div className="text-center text-muted-foreground text-xs py-8">
                  <FileText className="h-8 w-8 mx-auto mb-2 opacity-50" />
                  <p>No documents yet</p>
                  <p className="mt-1">Upload a PDF to start</p>
                </div>
              ) : (
                <div className="space-y-2">
                  {documents.map((doc, index) => (
                    <div
                      key={index}
                      className="p-2 rounded-lg border bg-card hover:bg-accent/50 transition-colors"
                    >
                      <div className="flex items-start gap-2">
                        <FileText className="h-4 w-4 mt-0.5 flex-shrink-0 text-primary" />
                        <div className="flex-1 min-w-0">
                          <p className="text-xs font-medium truncate" title={doc.filename}>
                            {doc.filename}
                          </p>
                          <p className="text-xs text-muted-foreground">
                            {formatFileSize(doc.size)}
                          </p>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </ScrollArea>
          </CardContent>
        </Card>
      </div>

      {/* Toggle Sidebar Button */}
      <Button
        variant="outline"
        size="sm"
        onClick={() => setSidebarOpen(!sidebarOpen)}
        className="absolute left-4 top-1/2 -translate-y-1/2 h-12 w-6 p-0 z-10"
      >
        {sidebarOpen ? <ChevronLeft className="h-4 w-4" /> : <ChevronRight className="h-4 w-4" />}
      </Button>

      {/* Main Chat Area */}
      <Card className="flex-1 flex flex-col">
        <CardHeader>
          <div className="flex items-center justify-between">
            <div>
              <CardTitle className="flex items-center gap-2">
                <BookOpen className="h-6 w-6" />
                RAG Chat Assistant
              </CardTitle>
              <CardDescription>
                Ask questions about your uploaded documents
              </CardDescription>
            </div>
            <div className="flex flex-col items-end gap-2 min-w-[200px]">
              <input
                ref={fileInputRef}
                type="file"
                accept=".pdf"
                onChange={handleFileUpload}
                className="hidden"
              />
              <div className="relative w-full">
                <Button
                  variant="outline"
                  size="sm"
                  onClick={() => fileInputRef.current?.click()}
                  disabled={uploading}
                  className="w-full relative overflow-hidden"
                >
                  {/* Progress bar background */}
                  {uploading && (
                    <div 
                      className="absolute inset-0 bg-primary/20 transition-all duration-300 ease-out"
                      style={{ width: `${uploadProgress}%` }}
                    />
                  )}
                  
                  {/* Button content */}
                  <span className="relative z-10 flex items-center justify-center">
                    {uploading ? (
                      <>
                        <Loader2 className="h-4 w-4 mr-2 animate-spin" />
                        {uploadProgress}%
                      </>
                    ) : (
                      <>
                        <Upload className="h-4 w-4 mr-2" />
                        Upload PDF
                      </>
                    )}
                  </span>
                </Button>
              </div>
              {uploadStatus && (
                <p className={`text-xs ${uploadStatus.startsWith('Error') ? 'text-red-500' : 'text-green-600'}`}>
                  {uploadStatus}
                </p>
              )}
            </div>
          </div>
        </CardHeader>
        
        <CardContent className="flex-1 flex flex-col gap-4">
          <ScrollArea className="flex-1 pr-4">
            <div className="space-y-4">
              {messages.length === 0 && (
                <div className="text-center text-muted-foreground py-8">
                  <Bot className="h-12 w-12 mx-auto mb-4 opacity-50" />
                  <p>Ask me anything about your documents!</p>
                  <p className="text-sm mt-2">Upload a PDF to get started</p>
                </div>
              )}
              
              {messages.map((message, index) => (
                <div
                  key={index}
                  className={`flex gap-3 ${
                    message.role === "user" ? "justify-end" : "justify-start"
                  }`}
                >
                  {message.role === "assistant" && (
                    <div className="flex-shrink-0">
                      <div className="h-8 w-8 rounded-full bg-primary flex items-center justify-center">
                        <Bot className="h-5 w-5 text-primary-foreground" />
                      </div>
                    </div>
                  )}
                  
                  <div
                    className={`flex flex-col gap-2 max-w-[80%] ${
                      message.role === "user" ? "items-end" : "items-start"
                    }`}
                  >
                    <div
                      className={`rounded-lg px-4 py-2 ${
                        message.role === "user"
                          ? "bg-primary text-primary-foreground"
                          : "bg-muted"
                      }`}
                    >
                      <p className="whitespace-pre-wrap">{message.content}</p>
                    </div>
                    
                    {message.context && message.context.length > 0 && (
                      <Button
                        variant="ghost"
                        size="sm"
                        onClick={() => setShowContext(!showContext)}
                        className="text-xs"
                      >
                        {showContext ? "Hide" : "Show"} context ({message.context.length})
                      </Button>
                    )}
                    
                    {showContext && message.context && (
                      <div className="w-full space-y-2">
                        {message.context.map((ctx, i) => (
                          <Card key={i} className="bg-secondary/50">
                            <CardContent className="p-3">
                              <p className="text-xs text-muted-foreground mb-1">
                                Context {i + 1}
                              </p>
                              <p className="text-sm">{ctx.substring(0, 200)}...</p>
                            </CardContent>
                          </Card>
                        ))}
                      </div>
                    )}
                  </div>
                  
                  {message.role === "user" && (
                    <div className="flex-shrink-0">
                      <div className="h-8 w-8 rounded-full bg-secondary flex items-center justify-center">
                        <User className="h-5 w-5" />
                      </div>
                    </div>
                  )}
                </div>
              ))}
              
              {loading && (
                <div className="flex gap-3 justify-start">
                  <div className="flex-shrink-0">
                    <div className="h-8 w-8 rounded-full bg-primary flex items-center justify-center">
                      <Bot className="h-5 w-5 text-primary-foreground" />
                    </div>
                  </div>
                  <div className="bg-muted rounded-lg px-4 py-2">
                    <Loader2 className="h-5 w-5 animate-spin" />
                  </div>
                </div>
              )}
            </div>
          </ScrollArea>
          
          <form onSubmit={handleSubmit} className="flex gap-2">
            <Input
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="Ask a question..."
              disabled={loading}
              className="flex-1"
            />
            <Button type="submit" disabled={loading || !input.trim()}>
              {loading ? (
                <Loader2 className="h-4 w-4 animate-spin" />
              ) : (
                <Send className="h-4 w-4" />
              )}
            </Button>
          </form>
        </CardContent>
      </Card>
    </div>
  )
}
