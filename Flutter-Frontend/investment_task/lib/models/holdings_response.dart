import 'holding.dart';
import 'portfolio_insights.dart';

class HoldingsResponse {
  final List<Holding> holdings;
  final PortfolioInsights insights;

  HoldingsResponse({
    required this.holdings,
    required this.insights,
  });

  factory HoldingsResponse.fromJson(Map<String, dynamic> json) {
    return HoldingsResponse(
      holdings: (json['holdings'] as List)
          .map((holding) => Holding.fromJson(holding))
          .toList(),
      insights: PortfolioInsights.fromJson(json['insights']),
    );
  }
}