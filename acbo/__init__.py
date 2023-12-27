#
#
#
# class Cocktail(Base):
#     __tablename__ = 'cocktail'
#
#     ID = Column(Integer, primary_key=True)
#     CocktailName = Column(String, nullable=False)
#     UsageCount = Column(Integer, default=0)
#
#
#
#
# class Spirit(Base):
#     __tablename__ = 'spirit'
#
#     ID = Column(Integer, primary_key=True)
#     Type = Column(Enum(SpiritType))
#     Measurement_ID = Column(Integer, ForeignKey('measurement.ID'))
#     UsageCount = Column(Integer, default=0)
#     cocktail_id = Column(Integer, ForeignKey('cocktail.ID'))
#
#     cocktail = relationship("Cocktail", backref="spirits")
#     measurement = relationship("Measurement")
#
# # ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ
#
# class Cocktail(Base):
#     __tablename__ = 'cocktail'
#
#     ID = Column(Integer, primary_key=True)
#     Spirit_id = Column(Integer, ForeignKey('spirit.ID'))
#     CocktailName = Column(String, nullable=False)
#     UsageCount = Column(Integer, default=0)
#
#     spirit = relationship("Spirit")
#
#
#
#
# class Spirit(Base):
#     __tablename__ = 'spirit'
#
#     ID = Column(Integer, primary_key=True)
#     Type = Column(Enum(SpiritType))
#     Measurement_ID = Column(Integer, ForeignKey('measurement.ID'))
#     UsageCount = Column(Integer, default=0)
#
#     cocktail = relationship("Cocktail")
#     measurement = relationship("Measurement")
#
#
#
#
#
# # Question
# def get_question(db: Session, question_id: int):
#     question = db.query(Question).get(question_id)
#     return question
#
#
# @router.get("/detail/{question_id}", response_model=question_schema.Question)
# def question_detail(question_id: int, db: Session = Depends(get_db)):
#     question = question_crud.get_question(db, question_id=question_id)
#     return question
#
#
# # Question 스키마
# class Question(BaseModel):
#     id: int
#     subject: str
#     content: str
#     create_date: datetime.datetime
#     answers: list[Answer] = []
#
#
# # Answer 스키마
# class Answer(BaseModel):
#     id: int
#     content: str
#     create_date: datetime.datetime
