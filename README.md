> 만든 사람: maduinos<br>
> 문서 만든 날짜: 2021-05-21<br>
> https://maduinos.blogspot.com/

# AutoTrading Lab

Maduinos의 개인 암호화폐 거래 연구 스크립트입니다.

이 저장소는 취미/실험 프로젝트이며 Maduinos FPGA 비즈니스 포트폴리오에 포함되지 않습니다. 실험 기록과 코드 정리 참고용으로 공개합니다.

## 안전 안내

- 이 저장소의 내용은 금융 조언이 아닙니다.
- 코드를 직접 검토하고 위험을 이해하기 전에는 실제 API key로 live trading 함수를 실행하지 마세요.
- API key는 절대 Git에 커밋하지 않습니다. 환경 변수로만 설정하세요.
- 읽기 전용 API 호출과 실제 주문 호출이 섞여 있던 과거 탐색용 스크립트는 공개 tree에서 제거했습니다.

## 요구 사항

- Python 3.10+
- live trading 함수를 의도적으로 실행할 때만 Upbit 계정 필요
- indicator 계산을 사용할 경우 TA-Lib native library 필요

Python package 설치:

```bash
python3 -m pip install -r requirements.txt
```

TA-Lib는 Python package 설치 전에 native library 설치가 필요할 수 있습니다:

```bash
tar -xzf ta-lib-0.4.0-src.tar.gz
cd ta-lib/
./configure --prefix=/usr
make
sudo make install
```

## API Key 설정

```bash
export UPBIT_ACCESS_KEY="<access-key>"
export UPBIT_SECRET_KEY="<secret-key>"
```

## 스크립트

| 파일 | 용도 |
| --- | --- |
| `autotrading.py` | 거래 helper, TA-Lib indicator 계산, 실험용 RSI strategy loop |
| `data_history.py` | 공개 candle history를 CSV 파일로 다운로드 |
| `get_mass_data.py` | pyupbit를 통해 더 큰 OHLCV dataset 다운로드 |

## 사용법

공개 candle CSV 다운로드:

```bash
python3 data_history.py --output-dir data --coins BTC ETH
```

더 큰 OHLCV 파일 다운로드:

```bash
python3 get_mass_data.py --ticker KRW-XRP --interval m1 --batches 10 --output mass_data.csv
```

소스를 검토하고 API key를 설정한 뒤에만 live strategy loop를 실행하세요:

```bash
python3 autotrading.py
```

## 라이선스

MIT License로 배포합니다. 자세한 내용은 `LICENSE`를 확인하세요.

## 프로젝트 관리

- 변경 이력: `CHANGELOG.md`
- 릴리스 절차: `RELEASE.md`
- 지원 범위: `SUPPORT.md`
- 기여 가이드: `CONTRIBUTING.md`
- 보안 이력 메모: `docs/security-history.md`
- 문의·소식: <https://maduinos.blogspot.com/>
