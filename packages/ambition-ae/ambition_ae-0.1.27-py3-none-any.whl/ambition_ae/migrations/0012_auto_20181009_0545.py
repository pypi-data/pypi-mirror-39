# Generated by Django 2.1 on 2018-10-09 03:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ambition_ae', '0011_auto_20181007_0053'),
    ]

    operations = [
        migrations.AddField(
            model_name='aefollowup',
            name='parent_action_item',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT,
                                    related_name='+', to='edc_action_item.ActionItem'),
        ),
        migrations.AddField(
            model_name='aefollowup',
            name='related_action_item',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT,
                                    related_name='+', to='edc_action_item.ActionItem'),
        ),
        migrations.AddField(
            model_name='aeinitial',
            name='parent_action_item',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT,
                                    related_name='+', to='edc_action_item.ActionItem'),
        ),
        migrations.AddField(
            model_name='aeinitial',
            name='related_action_item',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT,
                                    related_name='+', to='edc_action_item.ActionItem'),
        ),
        migrations.AddField(
            model_name='aetmg',
            name='parent_action_item',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT,
                                    related_name='+', to='edc_action_item.ActionItem'),
        ),
        migrations.AddField(
            model_name='aetmg',
            name='related_action_item',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT,
                                    related_name='+', to='edc_action_item.ActionItem'),
        ),
        migrations.AddField(
            model_name='historicalaefollowup',
            name='parent_action_item',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True,
                                    on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='edc_action_item.ActionItem'),
        ),
        migrations.AddField(
            model_name='historicalaefollowup',
            name='related_action_item',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True,
                                    on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='edc_action_item.ActionItem'),
        ),
        migrations.AddField(
            model_name='historicalaeinitial',
            name='parent_action_item',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True,
                                    on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='edc_action_item.ActionItem'),
        ),
        migrations.AddField(
            model_name='historicalaeinitial',
            name='related_action_item',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True,
                                    on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='edc_action_item.ActionItem'),
        ),
        migrations.AddField(
            model_name='historicalaetmg',
            name='parent_action_item',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True,
                                    on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='edc_action_item.ActionItem'),
        ),
        migrations.AddField(
            model_name='historicalaetmg',
            name='related_action_item',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True,
                                    on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='edc_action_item.ActionItem'),
        ),
        migrations.AddField(
            model_name='historicalrecurrencesymptom',
            name='parent_action_item',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True,
                                    on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='edc_action_item.ActionItem'),
        ),
        migrations.AddField(
            model_name='historicalrecurrencesymptom',
            name='related_action_item',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True,
                                    on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='edc_action_item.ActionItem'),
        ),
        migrations.AddField(
            model_name='recurrencesymptom',
            name='parent_action_item',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT,
                                    related_name='+', to='edc_action_item.ActionItem'),
        ),
        migrations.AddField(
            model_name='recurrencesymptom',
            name='related_action_item',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT,
                                    related_name='+', to='edc_action_item.ActionItem'),
        ),
        migrations.AlterField(
            model_name='aefollowup',
            name='action_identifier',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='aefollowup',
            name='parent_action_identifier',
            field=models.CharField(
                help_text='action identifier that links to parent reference model instance.', max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='aefollowup',
            name='related_action_identifier',
            field=models.CharField(
                help_text='action identifier that links to related reference model instance.', max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='aeinitial',
            name='action_identifier',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='aeinitial',
            name='parent_action_identifier',
            field=models.CharField(
                help_text='action identifier that links to parent reference model instance.', max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='aeinitial',
            name='related_action_identifier',
            field=models.CharField(
                help_text='action identifier that links to related reference model instance.', max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='aetmg',
            name='action_identifier',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='aetmg',
            name='parent_action_identifier',
            field=models.CharField(
                help_text='action identifier that links to parent reference model instance.', max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='aetmg',
            name='related_action_identifier',
            field=models.CharField(
                help_text='action identifier that links to related reference model instance.', max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='historicalaefollowup',
            name='action_identifier',
            field=models.CharField(null=True, max_length=50),
        ),
        migrations.AlterField(
            model_name='historicalaefollowup',
            name='parent_action_identifier',
            field=models.CharField(
                help_text='action identifier that links to parent reference model instance.', max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='historicalaefollowup',
            name='related_action_identifier',
            field=models.CharField(
                help_text='action identifier that links to related reference model instance.', max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='historicalaeinitial',
            name='action_identifier',
            field=models.CharField(null=True, max_length=50),
        ),
        migrations.AlterField(
            model_name='historicalaeinitial',
            name='parent_action_identifier',
            field=models.CharField(
                help_text='action identifier that links to parent reference model instance.', max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='historicalaeinitial',
            name='related_action_identifier',
            field=models.CharField(
                help_text='action identifier that links to related reference model instance.', max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='historicalaetmg',
            name='action_identifier',
            field=models.CharField(null=True, max_length=50),
        ),
        migrations.AlterField(
            model_name='historicalaetmg',
            name='parent_action_identifier',
            field=models.CharField(
                help_text='action identifier that links to parent reference model instance.', max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='historicalaetmg',
            name='related_action_identifier',
            field=models.CharField(
                help_text='action identifier that links to related reference model instance.', max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='historicalrecurrencesymptom',
            name='action_identifier',
            field=models.CharField(null=True, max_length=50),
        ),
        migrations.AlterField(
            model_name='historicalrecurrencesymptom',
            name='parent_action_identifier',
            field=models.CharField(
                help_text='action identifier that links to parent reference model instance.', max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='historicalrecurrencesymptom',
            name='related_action_identifier',
            field=models.CharField(
                help_text='action identifier that links to related reference model instance.', max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='recurrencesymptom',
            name='action_identifier',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='recurrencesymptom',
            name='parent_action_identifier',
            field=models.CharField(
                help_text='action identifier that links to parent reference model instance.', max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='recurrencesymptom',
            name='related_action_identifier',
            field=models.CharField(
                help_text='action identifier that links to related reference model instance.', max_length=30, null=True),
        ),
    ]
