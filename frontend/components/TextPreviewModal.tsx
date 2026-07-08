import { useEffect } from 'react';

interface Props {
  title: string;
  text: string;
  onDone: () => void;
}

function estimateRows(text: string, maxCharsPerLine: number, maxRows: number): number {
  const lineCount = text.split('\n').reduce((total, line) => {
    const estimatedWrapped = Math.ceil(Math.max(line.length, 1) / maxCharsPerLine);
    return total + Math.max(estimatedWrapped, 1);
  }, 0);

  return Math.max(1, Math.min(lineCount, maxRows));
}

export default function TextPreviewModal({ title, text, onDone }: Props) {
  useEffect(() => {
    const handleEscape = (event: KeyboardEvent) => {
      if (event.key === 'Escape') {
        onDone();
      }
    };

    document.addEventListener('keydown', handleEscape);
    return () => {
      document.removeEventListener('keydown', handleEscape);
    };
  }, [onDone]);

  const previewRows = estimateRows(text, 90, 16);

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50 p-4">
      <div className="w-full max-w-3xl rounded-lg bg-white p-5 shadow-xl">
        <h3 className="mb-3 text-lg font-semibold text-gray-900">{title}</h3>
        <textarea
          readOnly
          rows={previewRows}
          value={text}
          wrap="soft"
          className="w-full rounded-md border border-gray-300 bg-gray-50 p-3 text-sm text-gray-900 overflow-y-auto resize-none"
          aria-label={`${title} full text`}
        />
        <div className="mt-4 flex justify-end">
          <button
            type="button"
            onClick={onDone}
            className="rounded-md bg-blue-600 px-4 py-2 text-sm font-medium text-white hover:bg-blue-700"
          >
            Done
          </button>
        </div>
      </div>
    </div>
  );
}
