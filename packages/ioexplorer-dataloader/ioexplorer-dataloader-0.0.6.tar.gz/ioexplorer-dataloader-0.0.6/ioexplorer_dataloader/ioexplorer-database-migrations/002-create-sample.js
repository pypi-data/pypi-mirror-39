'use strict';
module.exports = {
  up: (queryInterface, Sequelize) => {
    return queryInterface.createTable('samples', {
      id: {
        primaryKey: true,
        autoIncrement: true,
        type: Sequelize.INTEGER,
        allowNull: false
      },
      subject_id: {
        type: Sequelize.INTEGER,
        references: {
          model: 'subjects',
          key: 'id'
        },
        onDelete: 'cascade'
      },
      sample_label: {
        type: Sequelize.STRING,
      },
      cancer_type: {
        type: Sequelize.STRING
      },
      cancer_type_detailed: {
        type: Sequelize.STRING
      },
      sample_type: {
        type: Sequelize.STRING
      },
      sample_class: {
        type: Sequelize.STRING
      },
      gene_panel: {
        type: Sequelize.STRING
      },
      sample_cover: {
        type: Sequelize.INTEGER
      },
      tumor_purity: {
        type: Sequelize.FLOAT
      },
      oncotree_code: {
        type: Sequelize.STRING
      },
      msi_score: {
        type: Sequelize.FLOAT
      },
      msi_type: {
        type: Sequelize.STRING
      },
      institute: {
        type: Sequelize.STRING
      },
      somatic_status: {
        type: Sequelize.STRING
      },
      // Exome Variables
      mutation_count: {
        type: Sequelize.INTEGER,
      },
      log10_mutation_count: {
        type: Sequelize.FLOAT,
      },
      neoantigen_count: {
        type: Sequelize.INTEGER,
      },
      neopeptide_count: {
        type: Sequelize.INTEGER,
      },
      aging_signature: {
        type: Sequelize.FLOAT,
      },
      uv_signature: {
        type: Sequelize.FLOAT,
      },
      davoli_scna: {
        type: Sequelize.FLOAT,
      },
      fraction_genome_cna: {
        type: Sequelize.FLOAT,
      },
      created_at: {
        allowNull: false,
        defaultValue: new Date(),
        type: Sequelize.DATE
      },
      updated_at: {
        allowNull: false,
        defaultValue: new Date(),
        type: Sequelize.DATE
      }
    }).then(() => {
      return queryInterface.addIndex('samples', {
        fields: ['subject_id']
      });
    });
  },
  down: (queryInterface, Sequelize) => {
    return queryInterface.dropTable('samples');
  }
};