# test.py
from custom_csv_reader import CustomCsvReader

def main():
    print("---- LLM STYLE RETRIEVAL ----")
    reader = CustomCsvReader("insurance_data.csv")

    while True:
        query = input("Ask your question (or type 'exit' to quit): ").strip()
        if query.lower() in ["exit", "quit"]:
            print("Exiting.")
            break
        result = reader.retrieve_information(query)
        print("\n" + result + "\n")

if __name__ == "__main__":
    main()
