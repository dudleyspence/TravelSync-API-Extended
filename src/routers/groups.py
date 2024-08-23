from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.schemas import GroupCreate, GroupResponse, GroupMemberCreate, GroupMemberResponse, UserResponse
from src.models import Group, GroupMember, User
from src.db.database import get_db
from typing import List

router = APIRouter()

@router.get('/', response_model=List[GroupResponse])
def get_groups(db: Session = Depends(get_db)) -> GroupResponse:
    db_groups = db.query(Group)
    return db_groups


@router.get('/{group_id}', response_model=GroupResponse)
def get_group_by_id(group_id: int, db: Session = Depends(get_db)) -> GroupResponse:
    db_group = db.query(Group).filter(Group.id == group_id).first()
    return db_group


@router.get('/{group_id}/members', response_model=List[UserResponse])
def get_group_members(group_id: int, db: Session = Depends(get_db)) -> List[UserResponse]:

    group_members = db.query(User).join(GroupMember, GroupMember.user_id == User.id).filter(GroupMember.group_id == group_id).all()
    
    if not group_members:
        raise HTTPException(status_code=404, detail="No members found for the specified group")

    return group_members

@router.post('/', response_model=GroupResponse)
def post_group(group: GroupCreate, db: Session = Depends(get_db)) -> GroupMemberResponse:
    new_group = Group(
        name=group.name,
    )

    db.add(new_group)
    db.commit()
    db.refresh(new_group)  

    return new_group

@router.post('/{group_id}/members', response_model=GroupMemberResponse)
def post_member_to_group(group_id: int, group_member: GroupMemberCreate, db: Session = Depends(get_db)) -> GroupMemberResponse:
    group = db.query(Group).filter(Group.id == group_id).first()
    if not group:
        raise HTTPException(status_code=404, detail="Sorry, this group does not exist")

    new_group_member = GroupMember(
        user_id = group_member.user_id,
        group_id = group_id,
    )

    existing_member = db.query(GroupMember).filter(
        GroupMember.group_id == group_id, 
        GroupMember.user_id == group_member.user_id
    ).first()
    
    if existing_member:
        raise HTTPException(status_code=400, detail="User is already a member of the group")


    db.add(new_group_member)
    db.commit()
    db.refresh(new_group_member)  

    return new_group_member

@router.delete('/{group_id}', response_model=GroupResponse)
def delete_group(group_id: int, db: Session = Depends(get_db)) -> GroupResponse:
    db_group = db.query(Group).filter(Group.id == group_id).first()
    if db_group is None:
        raise HTTPException(status_code=404, detail='Group not found')
    db.delete(db_group)
    db.commit()
    return db_group

@router.delete('/{group_id}/members/{user_id}', response_model=GroupMemberResponse)
def delete_member_from_group(group_id: int, user_id: int, db: Session = Depends(get_db)) -> GroupMemberResponse:
    db_member = db.query(GroupMember).filter(GroupMember.user_id == user_id, GroupMember.group_id == group_id).first()
    if db_member is None:
        raise HTTPException(status_code=404, detail='Group member not found')
    db.delete(db_member)
    db.commit()
    return db_member

@router.patch('/{group_id}', response_model=GroupResponse)
def update_group(group_id: int, group: GroupCreate, db: Session = Depends(get_db)) -> GroupMemberResponse:
    db_group = db.query(Group).filter(Group.id == group_id).first()

    if not db_group:
        raise HTTPException(status_code=404, detail="Group not found")

    group_data = group.model_dump(exclude_unset=True)
    for key, value in group_data.items():
        setattr(db_group, key, value)
    
    db.add(db_group)
    db.commit()
    db.refresh(db_group)
    
    return db_group