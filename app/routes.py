import logging
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.database import get_db, Bug
from app.schemas import BugResponse, BugListResponse, BugCreate, BugUpdate
from app.services import BugService

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/bugs", tags=["bugs"])


@router.get("/", response_model=BugListResponse)
async def list_bugs(
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    status: str = Query(None),
    severity: str = Query(None),
    notified: bool = Query(None)
):
    """
    Retrieve all bugs with pagination and filtering
    
    Query Parameters:
    - skip: Number of records to skip (default: 0)
    - limit: Number of records to return (default: 10, max: 100)
    - status: Filter by status (open, closed, etc.)
    - severity: Filter by severity (critical, high, medium, low)
    - notified: Filter by notification status
    """
    try:
        query = db.query(Bug)
        
        # Apply filters
        if status:
            query = query.filter(Bug.status == status)
        if severity:
            query = query.filter(Bug.severity == severity)
        if notified is not None:
            query = query.filter(Bug.notified == notified)
        
        # Get total count
        total = query.count()
        
        # Apply pagination
        bugs = query.offset(skip).limit(limit).all()
        
        total_pages = (total + limit - 1) // limit
        current_page = (skip // limit) + 1
        
        logger.info(f"Retrieved {len(bugs)} bugs (page {current_page})")
        
        return BugListResponse(
            total=total,
            items=[BugResponse.model_validate(bug) for bug in bugs],
            page=current_page,
            page_size=limit,
            total_pages=total_pages
        )
        
    except Exception as e:
        logger.error(f"Error retrieving bugs: {str(e)}")
        raise HTTPException(status_code=500, detail="Error retrieving bugs")


@router.get("/{bug_id}", response_model=BugResponse)
async def get_bug(bug_id: int, db: Session = Depends(get_db)):
    """Get a specific bug by ID"""
    try:
        bug = db.query(Bug).filter(Bug.id == bug_id).first()
        if not bug:
            raise HTTPException(status_code=404, detail="Bug not found")
        
        logger.info(f"Retrieved bug {bug_id}")
        return BugResponse.model_validate(bug)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving bug {bug_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Error retrieving bug")


@router.post("/", response_model=BugResponse)
async def create_bug(bug: BugCreate, db: Session = Depends(get_db)):
    """Create a new bug"""
    try:
        # Check if bug already exists
        existing = db.query(Bug).filter(Bug.external_id == bug.external_id).first()
        if existing:
            raise HTTPException(status_code=400, detail="Bug with this external_id already exists")
        
        new_bug = Bug(
            external_id=bug.external_id,
            title=bug.title,
            description=bug.description,
            severity=bug.severity,
            status=bug.status
        )
        db.add(new_bug)
        db.commit()
        db.refresh(new_bug)
        
        logger.info(f"Created new bug: {new_bug.id}")
        return BugResponse.model_validate(new_bug)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating bug: {str(e)}")
        db.rollback()
        raise HTTPException(status_code=500, detail="Error creating bug")


@router.put("/{bug_id}", response_model=BugResponse)
async def update_bug(bug_id: int, bug_update: BugUpdate, db: Session = Depends(get_db)):
    """Update a bug"""
    try:
        bug = db.query(Bug).filter(Bug.id == bug_id).first()
        if not bug:
            raise HTTPException(status_code=404, detail="Bug not found")
        
        update_data = bug_update.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(bug, field, value)
        
        db.commit()
        db.refresh(bug)
        
        logger.info(f"Updated bug {bug_id}")
        return BugResponse.model_validate(bug)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating bug {bug_id}: {str(e)}")
        db.rollback()
        raise HTTPException(status_code=500, detail="Error updating bug")


@router.delete("/{bug_id}")
async def delete_bug(bug_id: int, db: Session = Depends(get_db)):
    """Delete a bug"""
    try:
        bug = db.query(Bug).filter(Bug.id == bug_id).first()
        if not bug:
            raise HTTPException(status_code=404, detail="Bug not found")
        
        db.delete(bug)
        db.commit()
        
        logger.info(f"Deleted bug {bug_id}")
        return {"detail": "Bug deleted successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting bug {bug_id}: {str(e)}")
        db.rollback()
        raise HTTPException(status_code=500, detail="Error deleting bug")


@router.get("/stats/summary", response_model=dict)
async def get_stats(db: Session = Depends(get_db)):
    """Get bug statistics"""
    try:
        total = db.query(Bug).count()
        by_status = {}
        by_severity = {}
        
        statuses = db.query(Bug.status).distinct()
        for (status,) in statuses:
            by_status[status] = db.query(Bug).filter(Bug.status == status).count()
        
        severities = db.query(Bug.severity).distinct()
        for (severity,) in severities:
            by_severity[severity or "unknown"] = db.query(Bug).filter(Bug.severity == severity).count()
        
        notified = db.query(Bug).filter(Bug.notified == True).count()
        
        logger.info("Retrieved bug statistics")
        
        return {
            "total": total,
            "by_status": by_status,
            "by_severity": by_severity,
            "notified": notified,
            "unnotified": total - notified
        }
        
    except Exception as e:
        logger.error(f"Error retrieving stats: {str(e)}")
        raise HTTPException(status_code=500, detail="Error retrieving statistics")
