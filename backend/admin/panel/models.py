# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete`
#       set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create,
#       modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Handbook(models.Model):
    title = models.CharField(max_length=80, verbose_name="Название справочника")
    description = models.CharField(
        max_length=255, blank=True, null=True, verbose_name="Описание"
    )

    def __str__(self) -> str:
        return self.title

    class Meta:
        managed = True
        verbose_name = "Справочник"
        verbose_name_plural = "Справочники"
        db_table = "handbook"


class HandbookContent(models.Model):
    handbook = models.ForeignKey(Handbook, models.DO_NOTHING, verbose_name="Справочник")
    title = models.CharField(max_length=80, verbose_name="Название темы")
    text = models.TextField(verbose_name="Полный текст")
    reading_time = models.IntegerField()
    update_date = models.DateTimeField()
    create_date = models.DateTimeField()

    def __str__(self) -> str:
        return self.title

    class Meta:
        managed = True
        verbose_name = "Раздел справочника"
        verbose_name_plural = "Разделы справочника"
        db_table = "handbook_content"
