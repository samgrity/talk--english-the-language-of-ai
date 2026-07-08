#!/usr/bin/env bash
set -euo pipefail

SCRIPTS_DIR="$(cd "$(dirname "$0")" && pwd)"

echo "🧪 Running comprehensive test suite for HireFlow Candidate Screening System"
echo "======================================================================="

# Track test results
BACKEND_SUCCESS=0
FRONTEND_SUCCESS=0

echo ""
echo "📊 BACKEND TESTS"
echo "================="

if "$SCRIPTS_DIR/test-backend.sh"; then
  echo "✅ Backend tests PASSED"
  BACKEND_SUCCESS=1
else
  echo "❌ Backend tests FAILED"
fi

echo ""
echo "🎨 FRONTEND TESTS" 
echo "================="

if "$SCRIPTS_DIR/test-frontend.sh"; then
  echo "✅ Frontend tests PASSED"
  FRONTEND_SUCCESS=1
else
  echo "❌ Frontend tests FAILED"
fi

echo ""
echo "📋 TEST SUMMARY"
echo "==============="

if [ $BACKEND_SUCCESS -eq 1 ] && [ $FRONTEND_SUCCESS -eq 1 ]; then
  echo "🎉 ALL TESTS PASSED!"
  echo ""
  echo "✅ Backend API tests passed"
  echo "✅ Frontend component tests passed"
  echo "✅ TypeScript compilation successful"
  echo "✅ Build process successful"
  echo ""
  echo "System is ready for development and deployment! 🚀"
  exit 0
else
  echo "💥 SOME TESTS FAILED"
  echo ""
  if [ $BACKEND_SUCCESS -eq 0 ]; then
    echo "❌ Backend tests failed"
  fi
  if [ $FRONTEND_SUCCESS -eq 0 ]; then
    echo "❌ Frontend tests failed"
  fi
  echo ""
  echo "Please fix the failing tests before proceeding."
  exit 1
fi