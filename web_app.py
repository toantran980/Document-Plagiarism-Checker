from flask import Flask, render_template, request, redirect, url_for, jsonify
import os
from werkzeug.utils import secure_filename
import plagiarism_checker
from sample_algorithms import generate_huffman_codes
from sample_algorithms import build_huffman_tree, plot_huffman_tree
import io
import base64
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def highlight_text(content, words):
    if not words:
        return content
    # Simple whole-word replacement using boundaries
    import re
    def repl(match):
        return f"<mark>{match.group(0)}</mark>"

    for w in sorted(words, key=len, reverse=True):
        if not w:
            continue
        try:
            content = re.sub(rf'\b{re.escape(w)}\b', repl, content)
        except re.error:
            # fallback to simple replace
            content = content.replace(w, f"<mark>{w}</mark>")
    return content


@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    text1 = text2 = ''
    matches = set()
    similarity = 0.0
    huffman_info = None

    if request.method == 'POST':
        f1 = request.files.get('file1')
        f2 = request.files.get('file2')
        term = request.form.get('term', '').strip()

        path1 = path2 = None
        if f1 and f1.filename:
            filename1 = secure_filename(f1.filename)
            path1 = os.path.join(app.config['UPLOAD_FOLDER'], filename1)
            f1.save(path1)
            with open(path1, 'r', encoding='utf-8', errors='ignore') as fh:
                text1 = fh.read()

        if f2 and f2.filename:
            filename2 = secure_filename(f2.filename)
            path2 = os.path.join(app.config['UPLOAD_FOLDER'], filename2)
            f2.save(path2)
            with open(path2, 'r', encoding='utf-8', errors='ignore') as fh:
                text2 = fh.read()

        if path1 and path2:
            matches, similarity = plagiarism_checker.check_plagiarism(path1, path2)
        # Highlight matches and search term
        display1 = text1
        display2 = text2
        if matches:
            display1 = highlight_text(display1, matches)
            display2 = highlight_text(display2, matches)
        if term:
            display1 = highlight_text(display1, {term})
            display2 = highlight_text(display2, {term})

        # Huffman codes for doc1 if available else doc2
        source_text = text1 or text2
        if source_text:
            codes, enc, orig, comp = generate_huffman_codes(source_text)
            huffman_info = {'codes': dict(list(codes.items())[:200]), 'orig': orig, 'comp': comp}

        result = {'display1': display1, 'display2': display2, 'matches': list(matches), 'similarity': similarity, 'huffman': huffman_info, 'file1': os.path.basename(path1) if path1 else None, 'file2': os.path.basename(path2) if path2 else None}

    return render_template('index.html', result=result)


@app.route('/download_matches')
def download_matches():
    f1 = request.args.get('f1')
    f2 = request.args.get('f2')
    if not f1 or not f2:
        return "Missing file parameters", 400
    p1 = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(f1))
    p2 = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(f2))
    if not os.path.exists(p1) or not os.path.exists(p2):
        return "Files not found", 404
    matches, similarity = plagiarism_checker.check_plagiarism(p1, p2)
    text = "\n".join(sorted(list(matches)))
    return (text, 200, {'Content-Type': 'text/plain; charset=utf-8', 'Content-Disposition': f'attachment; filename="matches_{f1}_{f2}.txt"'})


@app.route('/download_huffman')
def download_huffman():
    f = request.args.get('f')
    if not f:
        return "Missing file parameter", 400
    p = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(f))
    if not os.path.exists(p):
        return "File not found", 404
    with open(p, 'r', encoding='utf-8', errors='ignore') as fh:
        text = fh.read()
    codes, enc, orig, comp = generate_huffman_codes(text)
    lines = [f"{repr(k)}: {v}" for k, v in sorted(codes.items())]
    body = "\n".join(lines)
    return (body, 200, {'Content-Type': 'text/plain; charset=utf-8', 'Content-Disposition': f'attachment; filename="huffman_{f}.txt"'})


@app.route('/export_json')
def export_json():
    f1 = request.args.get('f1')
    f2 = request.args.get('f2')
    if not f1 or not f2:
        return "Missing file parameters", 400
    p1 = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(f1))
    p2 = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(f2))
    if not os.path.exists(p1) or not os.path.exists(p2):
        return "Files not found", 404
    matches, similarity = plagiarism_checker.check_plagiarism(p1, p2)
    # Huffman for first file
    with open(p1, 'r', encoding='utf-8', errors='ignore') as fh:
        text = fh.read()
    codes, enc, orig, comp = generate_huffman_codes(text)
    payload = {
        'file1': f1,
        'file2': f2,
        'matches': sorted(list(matches)),
        'similarity': similarity,
        'huffman': {'codes': codes, 'original_bytes': orig, 'compressed_approx': comp}
    }
    return (jsonify(payload).get_data(as_text=True), 200, {'Content-Type': 'application/json; charset=utf-8', 'Content-Disposition': f'attachment; filename="report_{f1}_{f2}.json"'})


@app.route('/huffman_image')
def huffman_image():
    f = request.args.get('f')
    if not f:
        return "Missing file parameter", 400
    p = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(f))
    if not os.path.exists(p):
        return "File not found", 404
    with open(p, 'r', encoding='utf-8', errors='ignore') as fh:
        text = fh.read()
    # Build tree
    freq_map = {char: text.count(char) for char in set(text)}
    root = build_huffman_tree(freq_map)
    fig, ax = plt.subplots(figsize=(10, 6))
    # Use the existing plotting function; pass ax so it draws on our fig
    plot_huffman_tree(root, ax=ax)
    buf = io.BytesIO()
    fig.savefig(buf, format='png', bbox_inches='tight')
    plt.close(fig)
    buf.seek(0)
    return (buf.getvalue(), 200, {'Content-Type': 'image/png'})

    return render_template('index.html', result=result)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
