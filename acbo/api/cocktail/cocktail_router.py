from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from starlette import status

from api.cocktail import cocktail_crud, cocktail_schema
from api.user.user_router import get_current_superuser
from core.cloud_storage import upload_blob_from_memory
from db.database import get_db
from models import User

router = APIRouter(
    prefix="/api/cocktails",
    tags=["cocktail"],
)


@router.get("", response_model=cocktail_schema.CocktailList)
def cocktail_list(db: Session = Depends(get_db)):
    total, _cocktail_list = cocktail_crud.get_cocktail_list(db=db)
    return {'total': total, 'cocktails': _cocktail_list}


@router.get("/{cocktail_id:int}", response_model=cocktail_schema.CocktailDetail)
def cocktail_detail(cocktail_id: int, db: Session = Depends(get_db)):
    cocktail = cocktail_crud.get_cocktail(db=db, cocktail_id=cocktail_id)
    if not cocktail:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="존재하지 않는 Cocktail입니다.")
    return cocktail


@router.get("/{cocktail_id:int}/spirits", response_model=cocktail_schema.CocktailSpirits)
def cocktail_spirit_list(cocktail_id: int, db: Session = Depends(get_db)):
    if cocktail_crud.get_cocktail(db=db, cocktail_id=cocktail_id) is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="존재하지 않는 Cocktail입니다.")

    total, _cocktail_spirit_list = cocktail_crud.get_cocktail_spirit_list(db, cocktail_id=cocktail_id)
    if not _cocktail_spirit_list:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="등록된 Spirit이 없습니다.")
    return {'total': total, 'spirits': _cocktail_spirit_list}


@router.get("/{cocktail_id:int}/materials", response_model=cocktail_schema.CocktailMaterials)
def cocktail_material_list(cocktail_id: int, db: Session = Depends(get_db)):
    if cocktail_crud.get_cocktail(db=db, cocktail_id=cocktail_id) is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="존재하지 않는 Cocktail입니다.")

    total, _cocktail_material_list = cocktail_crud.get_cocktail_material_list(db, cocktail_id=cocktail_id)
    if not _cocktail_material_list:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="존재하지 않는 Cocktail입니다.")
    return {'total': total, 'materials': _cocktail_material_list}


@router.post("", status_code=status.HTTP_201_CREATED, response_model=None)
def cocktail_create(_cocktail_create: cocktail_schema.CocktailCreate,
                    db: Session = Depends(get_db),
                    superuser: User = Depends(get_current_superuser)):
    """
    ```json
    Args:
        _cocktail_create: {
            "name": "str", (NotNull)
            "name_ko": "str", (NotNull)
            "skill": "Stir", (Enum)
            "abv": 0, (1 이상)
        }
    Returns:

    """
    if not cocktail_crud.create_cocktail(db=db, cocktail=_cocktail_create):
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Cocktail을 생성하는데 실패했습니다.")
    return None


@router.put("/{cocktail_id}", status_code=status.HTTP_200_OK, response_model=None)
def cocktail_update(cocktail_id: int,
                    _cocktail_update: cocktail_schema.CocktailUpdate,
                    db: Session = Depends(get_db),
                    superuser: User = Depends(get_current_superuser)):
    cocktail = cocktail_crud.get_cocktail(db=db, cocktail_id=cocktail_id)
    if not cocktail:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="존재하지 않는 Cocktail입니다.")

    if not cocktail_crud.update_cocktail(db=db, db_cocktail=cocktail, cocktail_update=_cocktail_update):
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Cocktail을 수정하는데 실패했습니다.")
    return None


@router.delete("/{cocktail_id}", status_code=status.HTTP_204_NO_CONTENT)
def cocktail_delete(cocktail_id: int,
                    db: Session = Depends(get_db),
                    superuser: User = Depends(get_current_superuser)):
    if not cocktail_crud.get_cocktail(db=db, cocktail_id=cocktail_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="존재하지 않는 Cocktail입니다.")
    cocktail_crud.delete_cocktail(db=db, cocktail_id=cocktail_id)


@router.get("/", response_model=cocktail_schema.CocktailListBySpiritMaterial)
def cocktail_by_spirit_material(spirits: str | None = Query("", convert_underscores=False),
                                materials: str | None = Query("", convert_underscores=False),
                                db: Session = Depends(get_db)):
    """
    Frontend 칵테일 탭
    ```json
        {
            Args:
                spirits: (Query parameter, sep=",") default: "" -> 모든 Spirit
                    "Vodka,Whisky"
                materials: (Query parameter, sep=",") default: "" -> 모든 Material
                    "Liqueur:Triple Sec,Syrup:Simple"
            Returns:
                {
                  "total": 3,
                  "items": [
                    {
                      "name": "Russian Spring Punch",
                      "name_ko": "러시안 스프링 펀치",
                      "skill": "Shake",
                      "abv": 20
                    },
                    {
                      "name": "Long Island Iced Tea",
                      "name_ko": "롱 아일랜드 아이스 티",
                      "skill": "Build",
                      "abv": 20
                    },
                    {
                      "name": "Espresso Martini",
                      "name_ko": "에스프레소 마티니",
                      "skill": "Shake",
                      "abv": 25
                    }
                  ]
                }
        }
    ```
    """
    if spirits:
        # ["Vodka", "Whisky"]
        spirits = [spirit.capitalize() for spirit in spirits.split(",")]
    if materials:
        # [["Liqueur", "Triple_Sec"], ["Liqueur", "Blue_Curacao"], ["Syrup", "Simple_Syrup"]]
        materials = [x.split(":") for x in materials.replace(" ", "_").split(",")]
    total, cocktails = cocktail_crud.get_cocktail_by_spirit_material(spirits=spirits,
                                                                     materials=materials,
                                                                     db=db)
    if not cocktails:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cocktail을 찾을 수 없습니다.")
    return {"total": total, "items": cocktails}


@router.get("/{cocktail_name:str}", response_model=cocktail_schema.CocktailDetailByName)
def cocktail_detail_by_name(cocktail_name: str,
                            db: Session = Depends(get_db)):
    """
    Frontend 칵테일 상세 페이지
    """
    cocktail_name = cocktail_name.replace(" ", "_")
    cocktail = cocktail_crud.get_cocktail_detail_by_name(db=db, cocktail_name=cocktail_name)
    if not cocktail:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="존재하지 않는 Cocktail입니다.")
    return cocktail


@router.post("/request", status_code=status.HTTP_201_CREATED, response_model=None)
def cocktail_request(_cocktail_request: cocktail_schema.CocktailRequest):
    """
        칵테일 레시피 요청, GCS에 저장
        ```json
        Args:
            _cocktail_request: {
                "name": "str", (NotNull)
                "name_ko": "str", (NotNull)
                "skill": "Stir", (Enum)
                "abv": 0, (1 이상)
                "spirits": (Nullable) [
                    {
                        "type": "Vodka", (Enum)
                        "name": "str" || "", (Nullable)
                        "name_ko": "str" || "", (Nullable)
                        "unit": "ml", (Enum)
                        "amount": 0, (1 이상)
                    }
                ],
                "materials": (Nullable), default : []
                    {
                        "type": "Syrup", (Enum)
                        "name": "str", (NotNull)
                        "name_ko": "str", (NotNull)
                        "unit": "ml", (Enum)
                        "amount": 0, (1 이상)
                    }
                ]
            }
        Returns:
            Null
        ```
    """
    from fastapi.encoders import jsonable_encoder
    _cocktail_request = jsonable_encoder(_cocktail_request)  # str -> dict

    filename = _cocktail_request['name_ko']  # GCS에 저장할 파일명
    if not upload_blob_from_memory(bucket_name="acbo-request_recipes", data=_cocktail_request,
                                   destination_blob_name=filename):
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="칵테일 레시피를 요청하는데 실패했습니다."
                                                                                      "관리자에게 문의해주세요.")
    return None
