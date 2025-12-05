#!/bin/bash
# Automated script to run generator with predefined responses

# Responses:
# 1. Database choice: SQLite (1)
# 2. IGDB enrichment: No (N) - to speed up testing
# 3. Save to database: Yes (Y)

echo "Running generator with automated responses..."
echo "1" | python -m src.generator.generator << EOF
1
N
Y
EOF

echo ""
echo "Generator completed. Check reports/ directory for exports."
