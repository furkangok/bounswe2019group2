from django.core.management.base import BaseCommand
from django.utils import timezone
from ...models import Equipment, Parity
import datetime
import requests
import json
from decimal import *

YEAR_BEGIN = 2017


class Command(BaseCommand):
    help = 'Generates historic data related to parities'

    def add_arguments(self, parser):
        parser.add_argument('--demo', nargs='+', type=str,
                            help="Equipments to run the demo mode on")

    def _generate_parities(self, symbols=None):
        utc = timezone.utc
        today = datetime.datetime.utcnow().replace(tzinfo=utc).strftime('%Y-%m-%d')

        if symbols is None:
            result = requests.get("https://api.exchangeratesapi.io/%s" % today).json()
    
            symbols = list()
            symbols.append(result["base"])
            for key, _ in result["rates"].items():
                symbols.append(key)
    
        with open("./api/management/equipment.json") as f:
            maps = json.load(f)

        for symbol in symbols:
            if not Equipment.objects.filter(symbol=symbol).exists():
                Equipment(name=maps[symbol]["name"], category="Currency", symbol=symbol).save()

    def _write_currency_history(self, symbol, target_symbols=None):

        self.stdout.write("Getting %s data" % symbol)
        utc = timezone.utc
        today = datetime.datetime.utcnow().replace(tzinfo=utc).strftime('%Y-%m-%d')
        YEAR_END = int(today[:4])

        base_equipment = Equipment.objects.get(symbol=symbol)

        if target_symbols is None:
            target_symbols = Equipment.objects.values("symbol")

        for year in range(YEAR_BEGIN, YEAR_END + 1):

            begins = "%d-01-01" % year
            if year == YEAR_END:
                ends = today
            else:
                ends = "%d-01-01" % (year + 1)
            url = "https://api.exchangeratesapi.io/history?\
                                    start_at=%s&end_at=%s&base=%s" % (begins, ends, symbol)
            result = requests.get("https://api.exchangeratesapi.io/history?start_at=%s&end_at=%s&base=%s" %
                                  (begins, ends, symbol)).json()

            for date, rates in result["rates"].items():
                for target_symbol, rate in rates.items():

                    if target_symbol not in target_symbols:
                        continue

                    try:
                        target_equipment = Equipment.objects.get(symbol=target_symbol)
                    except _ as e:
                        self.stdout.write(e, target_symbol)

                    rate = Decimal(rate)

                    if not Parity.objects.filter(base_equipment=base_equipment, target_equipment=target_equipment,
                                                 date=date).exists():
                        rate = "%.3f" % rate
                        try:
                            Parity(base_equipment=base_equipment, target_equipment=target_equipment,
                                   ratio=rate, date=date).save()
                        except DecimalException as e:
                            self.stdout.write(str(e))

    def _generate_history(self):
        symbols = Equipment.objects.values("symbol")
        for symbol in symbols:
            self._write_currency_history(symbol["symbol"])

    def handle(self, *args, **options):
        if not options["demo"]:
            self._generate_parities()
            self._generate_history()

        else:
            self._generate_parities(options["demo"])
            for symbol in options["demo"]:
                self._write_currency_history(symbol, target_symbols=options["demo"])

        self.stdout.write('Generating historic data is done.')
