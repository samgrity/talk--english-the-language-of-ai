"use client";

import { useEffect, useMemo, useState } from 'react';
import { useRouter } from 'next/navigation';

import { getRecruiters } from '@/lib/api';
import { clearActiveRecruiter, setActiveRecruiter } from '@/lib/activeRecruiter';
import { Recruiter } from '@/types/api';

export default function LoginPage() {
  const router = useRouter();
  const [recruiters, setRecruiters] = useState<Recruiter[]>([]);
  const [nameQuery, setNameQuery] = useState('');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    clearActiveRecruiter();

    const loadRecruiters = async () => {
      try {
        setLoading(true);
        setError(null);
        const data = await getRecruiters();
        setRecruiters(data);
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Failed to load recruiters');
      } finally {
        setLoading(false);
      }
    };

    loadRecruiters();
  }, [router]);

  const filteredRecruiters = useMemo(() => {
    const query = nameQuery.trim().toLowerCase();
    if (!query) {
      return recruiters;
    }
    return recruiters.filter((recruiter) => recruiter.name.toLowerCase().includes(query));
  }, [nameQuery, recruiters]);

  const handleSelectRecruiter = (recruiter: Recruiter) => {
    setActiveRecruiter(recruiter);
    router.push('/queue');
  };

  return (
    <div className="min-h-screen bg-gray-50 flex items-center justify-center p-6">
      <div className="w-full max-w-xl rounded-lg bg-white shadow p-6">
        <h1 className="text-2xl font-bold text-gray-900">Recruiter Login</h1>
        <p className="mt-2 text-sm text-gray-600">
          Type your name and choose your recruiter profile to continue.
        </p>

        <div className="mt-4">
          <label htmlFor="recruiter-name" className="block text-sm font-medium text-gray-700 mb-1">
            Name
          </label>
          <input
            id="recruiter-name"
            type="text"
            value={nameQuery}
            onChange={(event) => setNameQuery(event.target.value)}
            placeholder="Start typing your name..."
            className="w-full rounded-md border border-gray-300 px-3 py-2 focus:border-blue-500 focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
        </div>

        <div className="mt-4 rounded-md border border-gray-200">
          {loading && <p className="p-4 text-sm text-gray-600">Loading recruiters...</p>}
          {!loading && error && <p className="p-4 text-sm text-red-700">Error: {error}</p>}
          {!loading && !error && filteredRecruiters.length === 0 && (
            <p className="p-4 text-sm text-gray-600">No recruiter matches your search.</p>
          )}
          {!loading && !error && filteredRecruiters.length > 0 && (
            <ul className="divide-y divide-gray-200">
              {filteredRecruiters.map((recruiter) => (
                <li key={recruiter.id} className="p-2">
                  <button
                    type="button"
                    onClick={() => handleSelectRecruiter(recruiter)}
                    className="w-full rounded-md px-3 py-2 text-left text-gray-900 hover:bg-gray-50"
                  >
                    {recruiter.name}
                  </button>
                </li>
              ))}
            </ul>
          )}
        </div>
      </div>
    </div>
  );
}
