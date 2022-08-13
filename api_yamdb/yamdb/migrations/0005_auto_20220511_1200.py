from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('yamdb', '0004_auto_20220510_2101'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='genre',
            name='name',
            field=models.CharField(max_length=100),
        ),
    ]
