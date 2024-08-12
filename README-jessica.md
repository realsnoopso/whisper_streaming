# 서버 실행

1. 프로젝트 디렉토리로 이동:

   ```
   cd /path/to/your/project
   ```

2. 가상 환경 생성 (선택사항이지만 권장):

   ```
   python -m venv myenv
   ```

3. 가상 환경 활성화:

   ```
   source myenv/bin/activate
   ```

4. requirements.txt에 나열된 모든 패키지 설치:

   ```
   pip install -r requirements.txt
   ```

5. 설치가 완료되면 서버 실행:

   ```
   python whisper_online_server.py --model small --min-chunk-size 0.5 --vad --language ko
   ```

# 클라이언트 실행

    ```
    python whisper_client.py
    ```
