import argparse, requests, csv, sys, datetime

URLS = {
    "lotofacil": "https://service.mobilon.com.br/api/loterias/lotofacil/last",
    "megasena":  "https://service.mobilon.com.br/api/loterias/megasena/last",
    "lotomania": "https://service.mobilon.com.br/api/loterias/lotomania/last"
}

def append_csv(loteria, csv_file):
    data = requests.get(URLS[loteria], timeout=10).json()
    concurso = data["numero"]
    dezenas  = sorted(data["dezenas"])
    date     = data["data"].split(" ")[0]   # yyyy-mm-dd
    # formato já usado por você
    with open(csv_file, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([concurso, date, *dezenas])
    print(f"✅ {loteria} {concurso} appendado")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--loteria", required=True)
    parser.add_argument("--output", default="loteria.csv")
    args = parser.parse_args()
    append_csv(args.loteria, args.output)