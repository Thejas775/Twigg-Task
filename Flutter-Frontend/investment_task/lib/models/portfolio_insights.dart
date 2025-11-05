class PortfolioInsights {
  final double totalCurrentValue;
  final double totalInvestmentCost;
  final double totalGainLoss;
  final double totalGainLossPercentage;

  PortfolioInsights({
    required this.totalCurrentValue,
    required this.totalInvestmentCost,
    required this.totalGainLoss,
    required this.totalGainLossPercentage,
  });

  factory PortfolioInsights.fromJson(Map<String, dynamic> json) {
    return PortfolioInsights(
      totalCurrentValue: double.parse(json['total_current_value'].toString()),
      totalInvestmentCost: double.parse(json['total_investment_cost'].toString()),
      totalGainLoss: double.parse(json['total_gain_loss'].toString()),
      totalGainLossPercentage: double.parse(json['total_gain_loss_percentage'].toString()),
    );
  }
}