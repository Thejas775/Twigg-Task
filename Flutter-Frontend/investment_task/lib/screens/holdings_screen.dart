import 'package:flutter/material.dart';
import '../services/api_service.dart';
import '../models/holdings_response.dart';
import '../models/holding.dart';
import '../models/portfolio_insights.dart';
import 'auth_screen.dart';

class HoldingsScreen extends StatefulWidget {
  const HoldingsScreen({super.key});

  @override
  State<HoldingsScreen> createState() => _HoldingsScreenState();
}

class _HoldingsScreenState extends State<HoldingsScreen> {
  final ApiService _apiService = ApiService();
  HoldingsResponse? _holdingsData;
  bool _isLoading = true;

  @override
  void initState() {
    super.initState();
    _loadHoldings();
  }

  Future<void> _loadHoldings() async {
    try {
      await _apiService.loadToken();
      final data = await _apiService.getHoldings();
      setState(() {
        _holdingsData = data;
        _isLoading = false;
      });
    } catch (e) {
      setState(() {
        _isLoading = false;
      });
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text('Failed to load holdings: ${e.toString()}')),
        );
      }
    }
  }

  Future<void> _logout() async {
    await _apiService.clearToken();
    if (mounted) {
      Navigator.of(context).pushReplacement(
        MaterialPageRoute(builder: (context) => const AuthScreen()),
      );
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('My Portfolio'),
        backgroundColor: Colors.blue[900],
        foregroundColor: Colors.white,
        actions: [
          IconButton(
            icon: const Icon(Icons.refresh),
            onPressed: () {
              setState(() {
                _isLoading = true;
              });
              _loadHoldings();
            },
          ),
          IconButton(
            icon: const Icon(Icons.logout),
            onPressed: _logout,
          ),
        ],
      ),
      body: _isLoading
          ? const Center(child: CircularProgressIndicator())
          : _holdingsData == null
              ? const Center(child: Text('Failed to load data'))
              : RefreshIndicator(
                  onRefresh: _loadHoldings,
                  child: SingleChildScrollView(
                    physics: const AlwaysScrollableScrollPhysics(),
                    padding: const EdgeInsets.all(16.0),
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        _buildInsightsCard(_holdingsData!.insights),
                        const SizedBox(height: 20),
                        const Text(
                          'Holdings',
                          style: TextStyle(
                            fontSize: 24,
                            fontWeight: FontWeight.bold,
                          ),
                        ),
                        const SizedBox(height: 16),
                        ..._holdingsData!.holdings.map((holding) => _buildHoldingCard(holding)),
                      ],
                    ),
                  ),
                ),
    );
  }

  Widget _buildInsightsCard(PortfolioInsights insights) {
    final isPositive = insights.totalGainLoss >= 0;

    return Card(
      elevation: 4,
      child: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            const Text(
              'Portfolio Overview',
              style: TextStyle(
                fontSize: 20,
                fontWeight: FontWeight.bold,
              ),
            ),
            const SizedBox(height: 16),
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                _buildInsightItem(
                  'Current Value',
                  '\$${insights.totalCurrentValue.toStringAsFixed(2)}',
                  Colors.blue,
                ),
                _buildInsightItem(
                  'Total Cost',
                  '\$${insights.totalInvestmentCost.toStringAsFixed(2)}',
                  Colors.grey,
                ),
              ],
            ),
            const SizedBox(height: 16),
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                _buildInsightItem(
                  'Gain/Loss',
                  '${isPositive ? '+' : ''}\$${insights.totalGainLoss.toStringAsFixed(2)}',
                  isPositive ? Colors.green : Colors.red,
                ),
                _buildInsightItem(
                  'Return',
                  '${isPositive ? '+' : ''}${insights.totalGainLossPercentage.toStringAsFixed(2)}%',
                  isPositive ? Colors.green : Colors.red,
                ),
              ],
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildInsightItem(String label, String value, Color color) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Text(
          label,
          style: const TextStyle(
            fontSize: 14,
            color: Colors.grey,
          ),
        ),
        Text(
          value,
          style: TextStyle(
            fontSize: 18,
            fontWeight: FontWeight.bold,
            color: color,
          ),
        ),
      ],
    );
  }

  Widget _buildHoldingCard(Holding holding) {
    final isPositive = holding.gainLoss >= 0;

    return Card(
      margin: const EdgeInsets.only(bottom: 12),
      child: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Row(
          children: [
            Container(
              width: 50,
              height: 50,
              decoration: BoxDecoration(
                color: _getAssetColor(holding.assetType),
                borderRadius: BorderRadius.circular(25),
              ),
              child: Icon(
                _getAssetIcon(holding.assetType),
                color: Colors.white,
                size: 24,
              ),
            ),
            const SizedBox(width: 16),
            Expanded(
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(
                    holding.assetSymbol,
                    style: const TextStyle(
                      fontSize: 18,
                      fontWeight: FontWeight.bold,
                    ),
                  ),
                  Text(
                    holding.assetName,
                    style: const TextStyle(
                      fontSize: 14,
                      color: Colors.grey,
                    ),
                  ),
                  const SizedBox(height: 4),
                  Text(
                    '${holding.quantity.toStringAsFixed(2)} shares',
                    style: const TextStyle(
                      fontSize: 12,
                      color: Colors.grey,
                    ),
                  ),
                ],
              ),
            ),
            Column(
              crossAxisAlignment: CrossAxisAlignment.end,
              children: [
                Text(
                  '\$${holding.currentValue.toStringAsFixed(2)}',
                  style: const TextStyle(
                    fontSize: 16,
                    fontWeight: FontWeight.bold,
                  ),
                ),
                Text(
                  '${isPositive ? '+' : ''}\$${holding.gainLoss.toStringAsFixed(2)}',
                  style: TextStyle(
                    fontSize: 14,
                    color: isPositive ? Colors.green : Colors.red,
                  ),
                ),
                Text(
                  '${isPositive ? '+' : ''}${holding.gainLossPercentage.toStringAsFixed(2)}%',
                  style: TextStyle(
                    fontSize: 12,
                    color: isPositive ? Colors.green : Colors.red,
                  ),
                ),
              ],
            ),
          ],
        ),
      ),
    );
  }

  Color _getAssetColor(String assetType) {
    switch (assetType.toLowerCase()) {
      case 'stock':
        return Colors.blue;
      case 'crypto':
        return Colors.orange;
      case 'etf':
        return Colors.green;
      default:
        return Colors.grey;
    }
  }

  IconData _getAssetIcon(String assetType) {
    switch (assetType.toLowerCase()) {
      case 'stock':
        return Icons.trending_up;
      case 'crypto':
        return Icons.currency_bitcoin;
      case 'etf':
        return Icons.account_balance;
      default:
        return Icons.attach_money;
    }
  }
}