export interface Statistics {
    totalRequests: number;
    resolvedRequests: number;
    averageResolutionTime: string;
    volumeLabels: string[];
    volumeData: number[];
    typeLabels: string[];
    typeData: number[];
    statusLabels: string[];
    statusData: number[];
  }
  
  export interface StatisticCard {
    period: string;
    label: string;
    value: number | string;
  }