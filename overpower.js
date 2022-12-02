import { serve } from "https://deno.land/std@0.166.0/http/server.ts";
import { serveDir } from "https://deno.land/std@0.166.0/http/file_server.ts"

const portNumber = 80;

serve(async (req) => {
    // console.log(req);

    // 日付関連
    const date = new Date();
    const formatted = date.toLocaleString();

    // reqあれこれ
    const method = req.method;
    const pathname = new URL(req.url).pathname;

    const dir = await serveDir(req, {
        fsRoot: "./public/",
        showDirListing: true,
        enableCors: true
    });

    // ここにAPIを実装
    //
    // if (pathname === "...")

    // 404 Not Found :(
    if (dir.status === 404) {
        const html = await Deno.readFile("./public/404.html");

        return new Response(html, {
            headers: {"Content-Type": "text/html"},
            status: 404,
            statusText: "404 Not Found"
        });
    }

    return dir;
}, { port: portNumber }).then();