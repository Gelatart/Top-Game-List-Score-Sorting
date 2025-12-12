#!/bin/bash

# Auto-test script for database changes
echo "🔍 Running database-related tests..."

# Activate virtual environment if it exists
if [ -d "venv" ]; then
    source venv/bin/activate
    echo "✅ Virtual environment activated"
fi

# Run the relevant tests
pytest tests/test_generator_seasonal.py tests/test_seasonal_attributes.py tests/test_file_loader.py \
    -v --tb=short --maxfail=3 --color=yes

exit_code=$?

if [ $exit_code -eq 0 ]; then
    echo "✅ All database tests passed!"
else
    echo "❌ Some tests failed (exit code: $exit_code)"
fi

exit $exit_code