from src.sentinelbert.inference.analyzer import LogAnalyzer

if __name__ == "__main__":
    analyzer = LogAnalyzer()

    sample_log = input("Enter log line: ")
    result = analyzer.predict(sample_log)

    print(result)