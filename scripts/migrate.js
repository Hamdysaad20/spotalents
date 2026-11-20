const fs = require('fs');
const path = require('path');
const { Client } = require('pg');

// Load environment variables from .env.local if present
const envLocalPath = path.join(__dirname, '../.env.local');
if (fs.existsSync(envLocalPath)) {
  const envContent = fs.readFileSync(envLocalPath, 'utf8');
  envContent.split('\n').forEach(line => {
    const match = line.match(/^\s*([\w.-]+)\s*=\s*(.*)?\s*$/);
    if (match) {
      let key = match[1];
      let value = (match[2] || '').trim();
      if (value.startsWith('"') && value.endsWith('"')) value = value.slice(1, -1);
      process.env[key] = value;
    }
  });
}

process.env.NODE_TLS_REJECT_UNAUTHORIZED = '0';

async function migrate() {
  const postgresUrl = process.env.POSTGRES_URL_NON_POOLING || process.env.POSTGRES_URL;
  if (!postgresUrl) {
    console.error('Error: POSTGRES_URL_NON_POOLING or POSTGRES_URL is not set in environment or .env.local');
    process.exit(1);
  }

  // Strip query parameters that might override custom ssl config
  const rawUrl = postgresUrl.split('?')[0];
  
  const client = new Client({
    connectionString: rawUrl,
    ssl: {
      rejectUnauthorized: false
    }
  });

  try {
    console.log('Connecting to Supabase PostgreSQL database...');
    await client.connect();
    console.log('Connected successfully!');

    const sqlPath = path.join(__dirname, '../supabase/schema.sql');
    const sql = fs.readFileSync(sqlPath, 'utf8');

    console.log('Applying schema.sql migration...');
    await client.query(sql);
    console.log('Schema applied successfully!');

    // Verify table exists
    const res = await client.query(`
      SELECT column_name, data_type, is_nullable
      FROM information_schema.columns
      WHERE table_name = 'leads'
      ORDER BY ordinal_position;
    `);

    console.log('\nVerified `leads` table columns:');
    res.rows.forEach(r => {
      console.log(` - ${r.column_name} (${r.data_type}, nullable: ${r.is_nullable})`);
    });

    // Verify RLS is enabled
    const rlsRes = await client.query(`
      SELECT relname, relrowsecurity, relforcerowsecurity 
      FROM pg_class 
      WHERE relname = 'leads';
    `);
    console.log('\nVerified Row Level Security (RLS):');
    rlsRes.rows.forEach(r => {
      console.log(` - Table: ${r.relname}, RLS Enabled: ${r.relrowsecurity}, Force RLS: ${r.relforcerowsecurity}`);
    });

    // Verify policies
    const polRes = await client.query(`
      SELECT policyname, cmd, roles 
      FROM pg_policies 
      WHERE tablename = 'leads';
    `);
    console.log('\nVerified Policies:');
    polRes.rows.forEach(r => {
      console.log(` - Policy: "${r.policyname}", Action: ${r.cmd}, Roles: ${r.roles}`);
    });

  } catch (err) {
    console.error('Migration failed:', err);
    process.exit(1);
  } finally {
    await client.end();
  }
}

migrate();
