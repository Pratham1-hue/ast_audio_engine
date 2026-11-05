from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.schemas import CodeAnalysisRequest, AnalysisResponse
from app.parser import ASTAnalyzer
from app.audio_mapper import map_ast_to_audio_tree

app = FastAPI(title="AST Audio Feedback Engine", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.post("/analyze", response_model=AnalysisResponse)
def analyze_code(payload: CodeAnalysisRequest):
    if not payload.code.strip():
        raise HTTPException(status_code=400, detail="Source code cannot be empty.")

    try:
        analyzer = ASTAnalyzer()
        raw_tree, total_nodes, max_depth = analyzer.parse_code(payload.code)
        processed_tree = map_ast_to_audio_tree(raw_tree)

        return AnalysisResponse(
            total_nodes=total_nodes,
            max_depth=max_depth,
            tree=processed_tree
        )
    except SyntaxError as e:
        raise HTTPException(status_code=422, detail=f"Syntax Error on line {e.lineno}: {e.msg}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))