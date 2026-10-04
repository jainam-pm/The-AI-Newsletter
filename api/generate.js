import { exec } from 'child_process';
import { promisify } from 'util';
import { readFileSync, writeFileSync } from 'fs';
import { join } from 'path';

const execAsync = promisify(exec);

export default async function handler(req, res) {
  // Only allow POST requests (from Vercel Cron)
  if (req.method !== 'POST' && req.method !== 'GET') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  try {
    console.log('[INFO] Starting newsletter generation at', new Date().toISOString());

    // Set environment variables for Supabase
    process.env.SUPABASE_URL = process.env.SUPABASE_URL;
    process.env.SUPABASE_ANON_KEY = process.env.SUPABASE_ANON_KEY;

    // Execute the Python editor.py script
    const { stdout, stderr } = await execAsync('python3 editor.py', {
      cwd: process.cwd(),
      timeout: 60000, // 60 second timeout
      maxBuffer: 10 * 1024 * 1024 // 10 MB buffer
    });

    console.log('[STDOUT]', stdout);
    if (stderr) console.log('[STDERR]', stderr);

    // Read the generated newsletter
    const newsletterPath = join(process.cwd(), 'output', 'newsletter-final.html');
    const newsletter = readFileSync(newsletterPath, 'utf-8');

    return res.status(200).json({
      success: true,
      message: 'Newsletter generated successfully',
      timestamp: new Date().toISOString(),
      size: newsletter.length,
      output: stdout
    });

  } catch (error) {
    console.error('[ERROR]', error);
    return res.status(500).json({
      success: false,
      error: error.message,
      timestamp: new Date().toISOString()
    });
  }
}
