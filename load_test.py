import requests
import concurrent.futures
import time
import json

BASE_URL = "http://localhost:5000"

def send_async_request(request_id, docx_path):
    """Send an async request and track its completion"""
    try:
        start_time = time.time()
        
        # Send async request
        with open(docx_path, 'rb') as f:
            files = {'file': f}
            response = requests.post(f"{BASE_URL}/api/quiz?async=true", files=files)
        
        if response.status_code != 202:
            return {
                "request_id": request_id,
                "error": f"Failed to submit: {response.status_code}",
                "total_time": time.time() - start_time
            }
        
        task_data = response.json()
        task_id = task_data['task_id']
        
        # Poll for completion
        while True:
            status_response = requests.get(f"{BASE_URL}/api/status/{task_id}")
            if status_response.status_code != 200:
                return {
                    "request_id": request_id,
                    "task_id": task_id,
                    "error": "Failed to check status",
                    "total_time": time.time() - start_time
                }
            
            status_data = status_response.json()
            
            if status_data['status'] == 'completed':
                return {
                    "request_id": request_id,
                    "task_id": task_id,
                    "status": "success",
                    "questions_count": len(status_data['result']['questions']),
                    "processing_time": status_data.get('processing_time', 0),
                    "total_time": time.time() - start_time
                }
            elif status_data['status'] == 'failed':
                return {
                    "request_id": request_id,
                    "task_id": task_id,
                    "status": "failed",
                    "error": status_data.get('error', 'Unknown error'),
                    "total_time": time.time() - start_time
                }
            
            time.sleep(0.5)  # Check every 0.5 seconds
    
    except Exception as e:
        return {
            "request_id": request_id,
            "error": str(e),
            "total_time": time.time() - start_time
        }

def test_concurrent_load(docx_path, num_requests=20):
    """Test server with concurrent requests"""
    print(f"Bắt đầu test với {num_requests} requests đồng thời...")
    print("=" * 60)
    
    # Check server status before
    try:
        response = requests.get(f"{BASE_URL}/api/server-status")
        print("Server status trước khi test:")
        print(json.dumps(response.json(), indent=2))
        print("-" * 40)
    except:
        print("Không thể connect đến server!")
        return
    
    start_time = time.time()
    
    # Send concurrent requests
    with concurrent.futures.ThreadPoolExecutor(max_workers=num_requests) as executor:
        futures = [
            executor.submit(send_async_request, i+1, docx_path) 
            for i in range(num_requests)
        ]
        
        results = []
        for future in concurrent.futures.as_completed(futures):
            result = future.result()
            results.append(result)
            print(f"Request {result['request_id']}: {result.get('status', 'error')} "
                  f"- Time: {result['total_time']:.2f}s")
    
    total_time = time.time() - start_time
    
    # Analyze results
    print("\n" + "=" * 60)
    print("KẾT QUẢ PHÂN TÍCH:")
    print(f"Tổng thời gian: {total_time:.2f}s")
    print(f"Số requests: {num_requests}")
    
    successful = [r for r in results if r.get('status') == 'success']
    failed = [r for r in results if r.get('status') == 'failed']
    errors = [r for r in results if 'error' in r and r.get('status') != 'failed']
    
    print(f"Thành công: {len(successful)}")
    print(f"Thất bại: {len(failed)}")
    print(f"Lỗi: {len(errors)}")
    
    if successful:
        avg_processing = sum(r.get('processing_time', 0) for r in successful) / len(successful)
        avg_total = sum(r['total_time'] for r in successful) / len(successful)
        print(f"Thời gian xử lý trung bình: {avg_processing:.2f}s")
        print(f"Thời gian tổng trung bình: {avg_total:.2f}s")
    
    # Check server status after
    try:
        time.sleep(2)  # Wait a bit
        response = requests.get(f"{BASE_URL}/api/server-status")
        print("\nServer status sau khi test:")
        print(json.dumps(response.json(), indent=2))
    except:
        print("Không thể check server status sau test!")

if __name__ == "__main__":
    print("CONCURRENT LOAD TESTER")
    print("=" * 60)
    
    docx_path = input("Nhập đường dẫn file .docx: ").strip()
    
    if not docx_path.endswith('.docx'):
        print("File phải có extension .docx!")
        exit(1)
    
    try:
        num_requests = int(input("Số lượng concurrent requests (mặc định 10): ") or "10")
    except:
        num_requests = 10
    
    test_concurrent_load(docx_path, num_requests)
