#!/bin/bash
echo "============================================"
echo " Smartwatch Analyzer - Frontend (Streamlit)"
echo "============================================"
echo ""
echo "Web app is available at: http://localhost:3000"
echo ""
echo "--------------------------------------------"
echo ""

exec streamlit run app.py --server.address 0.0.0.0 --server.port 8501
