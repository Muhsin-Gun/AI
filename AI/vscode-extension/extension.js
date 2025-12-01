const vscode = require('vscode');
const axios = require('axios');
const os = require('os');
const path = require('path');

const API_BASE = "http://127.0.0.1:5000";

function activate(context) {
    let chat = vscode.commands.registerCommand('myLocalAI.chat', async function () {
        const q = await vscode.window.showInputBox({prompt: 'Ask the AI (chat):'});
        if (!q) return;
        try {
            const r = await axios.post(`${API_BASE}/chat`, {text: q});
            vscode.window.showInformationMessage('AI: ' + r.data.response);
        } catch (err) {
            vscode.window.showErrorMessage('Error calling AI: ' + err.message);
        }
    });

    let analyze = vscode.commands.registerCommand('myLocalAI.analyzeFile', async function () {
        const editor = vscode.window.activeTextEditor;
        if (!editor) {
            vscode.window.showErrorMessage('Open a file first');
            return;
        }
        const filePath = editor.document.uri.fsPath;
        try {
            const r = await axios.post(`${API_BASE}/analyze_file`, {path: filePath});
            const doc = r.data.analysis || JSON.stringify(r.data);
            vscode.window.showInformationMessage('Analysis produced (first 300 chars): ' + doc.substring(0,300));
            const docWin = await vscode.workspace.openTextDocument({content: doc, language: 'markdown'});
            vscode.window.showTextDocument(docWin, {preview:false});
        } catch (err) {
            vscode.window.showErrorMessage('Error analyzing file: ' + err.message);
        }
    });

    let applyPatch = vscode.commands.registerCommand('myLocalAI.applyPatch', async function () {
        const patch = await vscode.window.showInputBox({prompt: 'Paste unified diff patch to apply:'});
        if (!patch) return;
        try {
            const r = await axios.post(`${API_BASE}/apply_patch`, {patch: patch});
            vscode.window.showInformationMessage('Apply patch result: ' + JSON.stringify(r.data));
        } catch (err) {
            vscode.window.showErrorMessage('Error applying patch: ' + err.message);
        }
    });

    let runCommand = vscode.commands.registerCommand('myLocalAI.runCommand', async function () {
        const cmd = await vscode.window.showInputBox({prompt: 'Shell command to run (cwd: workspace root):'});
        if (!cmd) return;
        try {
            const r = await axios.post(`${API_BASE}/run_command`, {command: cmd});
            const out = JSON.stringify(r.data, null, 2);
            const docWin = await vscode.workspace.openTextDocument({content: out, language: 'json'});
            vscode.window.showTextDocument(docWin, {preview:false});
        } catch (err) {
            vscode.window.showErrorMessage('Error running command: ' + err.message);
        }
    });

    context.subscriptions.push(chat, analyze, applyPatch, runCommand);
}
exports.activate = activate;
function deactivate() {}
exports.deactivate = deactivate;
