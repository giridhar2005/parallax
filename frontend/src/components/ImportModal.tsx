import React, { useState, useRef } from "react";
import { X, Upload, FileVideo, FileText, Loader2, CheckCircle2 } from "lucide-react";

interface ImportModalProps {
  isOpen: boolean;
  onClose: () => void;
  onImport: (file: File) => Promise<void>;
}

export const ImportModal: React.FC<ImportModalProps> = ({
  isOpen,
  onClose,
  onImport,
}) => {
  const [isUploading, setIsUploading] = useState<boolean>(false);
  const [successMsg, setSuccessMsg] = useState<string | null>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);

  if (!isOpen) return null;

  const handleFileChange = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    setIsUploading(true);
    setSuccessMsg(null);
    try {
      await onImport(file);
      setSuccessMsg(`Successfully imported ${file.name}`);
      setTimeout(() => {
        setSuccessMsg(null);
        onClose();
      }, 1500);
    } catch (err) {
      alert("Failed to import media file.");
    } finally {
      setIsUploading(false);
    }
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/75 backdrop-blur-sm select-none">
      <div className="w-full max-w-md bg-[#111113] border border-[#27272A] rounded shadow-2xl overflow-hidden font-mono text-xs">
        {/* Header */}
        <div className="p-3 border-b border-[#27272A] flex items-center justify-between bg-[#0E0E10]">
          <div className="flex items-center space-x-2 text-zinc-200">
            <Upload className="w-4 h-4 text-rose-500" />
            <span className="font-semibold text-sm">Import Forensic Evidence</span>
          </div>
          <button
            onClick={onClose}
            className="p-1 rounded text-zinc-500 hover:text-white transition"
          >
            <X className="w-4 h-4" />
          </button>
        </div>

        {/* Upload Drop Zone */}
        <div className="p-6 space-y-4">
          <input
            type="file"
            ref={fileInputRef}
            onChange={handleFileChange}
            accept=".mp4,.mov,.pdf,.mp3,.wav"
            className="hidden"
          />

          <div
            onClick={() => fileInputRef.current?.click()}
            className="border-2 border-dashed border-[#27272A] hover:border-rose-500/60 rounded-lg p-8 flex flex-col items-center justify-center cursor-pointer transition bg-[#09090B] space-y-3"
          >
            <div className="flex items-center space-x-2 text-zinc-500">
              <FileVideo className="w-6 h-6 text-zinc-400" />
              <span className="text-zinc-600">+</span>
              <FileText className="w-6 h-6 text-zinc-400" />
            </div>

            <div className="text-center space-y-1">
              <p className="font-semibold text-zinc-200">
                Click to browse or drop forensic files
              </p>
              <p className="text-[11px] text-zinc-500">
                Supports Deposition Video (.mp4, .mov) and Evidentiary PDFs (.pdf)
              </p>
            </div>

            {isUploading && (
              <div className="flex items-center space-x-2 text-rose-400 pt-2">
                <Loader2 className="w-4 h-4 animate-spin" />
                <span>Ingesting into SQLite WAL & LanceDB...</span>
              </div>
            )}

            {successMsg && (
              <div className="flex items-center space-x-2 text-emerald-400 pt-2">
                <CheckCircle2 className="w-4 h-4" />
                <span>{successMsg}</span>
              </div>
            )}
          </div>

          <div className="text-[11px] text-zinc-500 text-center leading-relaxed">
            Imported files are hashed with SHA-256 and stored persistently inside{" "}
            <code className="text-zinc-400">~/Library/Application Support/Parallax/raw/</code>.
          </div>
        </div>
      </div>
    </div>
  );
};
