from flask import Flask, render_template, request, jsonify, send_file, url_for
import os
import subprocess
import threading
import time
from pathlib import Path
import uuid
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 500 * 1024 * 1024  # 500MB 제한
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['OUTPUT_FOLDER'] = 'outputs'

# 업로드 및 출력 폴더 생성
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['OUTPUT_FOLDER'], exist_ok=True)

# 지원되는 비디오 포맷
ALLOWED_EXTENSIONS = {'mp4', 'avi', 'mov', 'mkv', 'wmv', 'flv', 'webm', 'm4v', '3gp'}
OUTPUT_FORMATS = {
    'mp4': {'ext': '.mp4', 'codec': 'libx264'},
    'avi': {'ext': '.avi', 'codec': 'libx264'},
    'mov': {'ext': '.mov', 'codec': 'libx264'},
    'webm': {'ext': '.webm', 'codec': 'libvpx-vp9'},
    'mkv': {'ext': '.mkv', 'codec': 'libx264'}
}

# 압축 작업 상태 저장
compression_status = {}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': '파일이 선택되지 않았습니다.'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': '파일이 선택되지 않았습니다.'}), 400
    
    if not allowed_file(file.filename):
        return jsonify({'error': '지원되지 않는 파일 형식입니다.'}), 400
    
    # 고유한 작업 ID 생성
    job_id = str(uuid.uuid4())
    
    # 파일 저장
    filename = secure_filename(file.filename)
    input_path = os.path.join(app.config['UPLOAD_FOLDER'], f"{job_id}_{filename}")
    file.save(input_path)
    
    # 파일 크기 확인
    file_size = os.path.getsize(input_path) / (1024 * 1024)  # MB
    
    return jsonify({
        'job_id': job_id,
        'filename': filename,
        'file_size': round(file_size, 2)
    })

@app.route('/compress', methods=['POST'])
def compress_video():
    data = request.json
    job_id = data.get('job_id')
    quality = data.get('quality', 'medium')
    resolution = data.get('resolution', 'original')
    output_format = data.get('output_format', 'mp4')
    
    if not job_id or job_id not in [f.split('_')[0] for f in os.listdir(app.config['UPLOAD_FOLDER'])]:
        return jsonify({'error': '유효하지 않은 작업 ID입니다.'}), 400
    
    # 입력 파일 찾기
    input_file = None
    for f in os.listdir(app.config['UPLOAD_FOLDER']):
        if f.startswith(job_id):
            input_file = os.path.join(app.config['UPLOAD_FOLDER'], f)
            break
    
    if not input_file:
        return jsonify({'error': '입력 파일을 찾을 수 없습니다.'}), 404
    
    # 출력 파일 경로 생성
    original_name = Path(input_file).stem.split('_', 1)[1]  # job_id 제거
    output_ext = OUTPUT_FORMATS[output_format]['ext']
    output_file = os.path.join(app.config['OUTPUT_FOLDER'], f"{job_id}_compressed_{original_name}{output_ext}")
    
    # 압축 상태 초기화
    compression_status[job_id] = {
        'status': 'processing',
        'progress': 0,
        'message': '압축 준비 중...',
        'output_file': output_file,
        'start_time': time.time()
    }
    
    # 백그라운드에서 압축 실행
    thread = threading.Thread(target=compress_video_background, 
                            args=(job_id, input_file, output_file, quality, resolution, output_format))
    thread.daemon = True
    thread.start()
    
    return jsonify({'job_id': job_id, 'status': 'started'})

def compress_video_background(job_id, input_file, output_file, quality, resolution, output_format):
    try:
        # FFmpeg 명령어 구성
        cmd = ['ffmpeg', '-i', input_file]
        
        # 품질 설정
        quality_settings = {
            'high': '18',
            'medium': '23',
            'low': '28'
        }
        cmd.extend(['-crf', quality_settings[quality]])
        
        # 해상도 설정
        if resolution != 'original':
            resolution_map = {
                '1080p': '1920:1080',
                '720p': '1280:720',
                '480p': '854:480',
                '360p': '640:360'
            }
            cmd.extend(['-vf', f'scale={resolution_map[resolution]}'])
        
        # 코덱 설정
        codec = OUTPUT_FORMATS[output_format]['codec']
        cmd.extend(['-c:v', codec])
        
        # 오디오 코덱
        if output_format == 'webm':
            cmd.extend(['-c:a', 'libvorbis'])
        else:
            cmd.extend(['-c:a', 'aac'])
        
        # 출력 파일
        cmd.extend(['-y', output_file])
        
        # 상태 업데이트
        compression_status[job_id]['message'] = '압축 중...'
        compression_status[job_id]['progress'] = 50
        
        # FFmpeg 실행
        process = subprocess.run(cmd, capture_output=True, text=True)
        
        if process.returncode == 0:
            # 성공
            input_size = os.path.getsize(input_file) / (1024 * 1024)
            output_size = os.path.getsize(output_file) / (1024 * 1024)
            reduction = ((input_size - output_size) / input_size) * 100
            
            compression_status[job_id].update({
                'status': 'completed',
                'progress': 100,
                'message': '압축 완료!',
                'input_size': round(input_size, 2),
                'output_size': round(output_size, 2),
                'reduction': round(reduction, 1),
                'end_time': time.time()
            })
        else:
            # 실패
            compression_status[job_id].update({
                'status': 'failed',
                'progress': 0,
                'message': f'압축 실패: {process.stderr}',
                'error': process.stderr
            })
            
    except Exception as e:
        compression_status[job_id].update({
            'status': 'failed',
            'progress': 0,
            'message': f'오류 발생: {str(e)}',
            'error': str(e)
        })

@app.route('/status/<job_id>')
def get_status(job_id):
    if job_id not in compression_status:
        return jsonify({'error': '작업을 찾을 수 없습니다.'}), 404
    
    return jsonify(compression_status[job_id])

@app.route('/download/<job_id>')
def download_file(job_id):
    if job_id not in compression_status:
        return jsonify({'error': '작업을 찾을 수 없습니다.'}), 404
    
    status = compression_status[job_id]
    if status['status'] != 'completed':
        return jsonify({'error': '압축이 완료되지 않았습니다.'}), 400
    
    output_file = status['output_file']
    if not os.path.exists(output_file):
        return jsonify({'error': '출력 파일을 찾을 수 없습니다.'}), 404
    
    return send_file(output_file, as_attachment=True, download_name=os.path.basename(output_file))

@app.route('/cleanup/<job_id>', methods=['DELETE'])
def cleanup_files(job_id):
    # 입력 파일 삭제
    for f in os.listdir(app.config['UPLOAD_FOLDER']):
        if f.startswith(job_id):
            try:
                os.remove(os.path.join(app.config['UPLOAD_FOLDER'], f))
            except:
                pass
    
    # 출력 파일 삭제
    if job_id in compression_status:
        output_file = compression_status[job_id].get('output_file')
        if output_file and os.path.exists(output_file):
            try:
                os.remove(output_file)
            except:
                pass
        
        # 상태 삭제
        del compression_status[job_id]
    
    return jsonify({'status': 'cleaned'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)