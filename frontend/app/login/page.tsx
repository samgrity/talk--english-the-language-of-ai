"use client";

import { useEffect } from 'react';
import { useRouter } from 'next/navigation';

export default function LoginPage() {
  const router = useRouter();

  useEffect(() => {
    router.replace('/queue');
  }, [router]);

  return (
    <div className="min-h-screen bg-gray-50 flex items-center justify-center p-6">
      <div className="w-full max-w-xl rounded-lg bg-white shadow p-6 text-center">
        <h1 className="text-2xl font-bold text-gray-900">HireFlow</h1>
        <p className="mt-2 text-sm text-gray-600">
          Redirecting to the candidate pipeline...
        </p>
      </div>
    </div>
  );
}
