# FINAL_EXECUTION_REPORT

Method: Two-agent stochastic dynamic investment game with generalized Nash bargaining and surrogate-assisted equilibrium mapping.

Status: ALL_STAGES_COMPLETED

## Reproducibility

```json
{
  "git_commit": null,
  "git_status_note": "NOT_A_GIT_REPOSITORY",
  "config_sha256": "3b928b7fa65ee90acf52fe1c968de855cddddf3c81b5a2661d9ffd134bd48e76",
  "source_manifest_hash": "1d8388dd180a3b528d8a7fe66fdee6fb8886d5a28c760b9aec3e1ea86e439d0b",
  "source_files_sha256": {
    "src/__init__.py": "5d9910ba4a052768c2b365fbb1c193fdf8ad691e274d6f3b89a830dd590ab655",
    "src/bargaining.py": "39abe1e7a04c168cfd0681d4b99e986e5c85d53c4a5307cbdf4da0292586bc4b",
    "src/boundary.py": "fc0e43ec7c95e6319a140b70b86a3b0988cf5398f1ddfc01a0a787d52410f57f",
    "src/carbon_tree.py": "82760f479ee4f39d3a0e5111c8ebb2492a84592fd4937cff3ee05fd10920b5c5",
    "src/config.py": "43dda3d9448a3183a3ee6e0c2f5eda17032194c9f0bcfd0ce770b769b3df147c",
    "src/dataset.py": "4d86522af749bafd2ad1f5ef023357f7682c255d9a1bc89d34dd90ca25aabdc5",
    "src/dynamic_solver.py": "e095e582b660d84858931c1f33773d4809ee7be4af4850d55143a4b2d7001b29",
    "src/economics.py": "36fbe22c395ab8b4eb329b0075b29ddabf7faf500eeb78578686a39f4b63d168",
    "src/equilibrium_selection.py": "63adaea32b6b152f93a7936257e0cc24e3a5cb926792521fecf9c36ecf1e6852",
    "src/forward_propagation.py": "920fd393dbda9b1dcc3fd344eadffc0e7540adddce56b6d9b1b599707370d4d2",
    "src/metrics.py": "860830e7504d7d371cfd494cc5cfe8bf2fb781860a48b58d0cde71c830597cc1",
    "src/protocol.py": "d58a1d63710255c28b389c13f89a1f9c84bf7ea44e81c84b61774aa5e02b204f",
    "src/reproducibility.py": "fd45c087052a1476ffd237abadb19a41a749a864a70ebef974fbbc7a7575c8d3",
    "src/scenario_solver.py": "2eeba38c70747d659b6dc0003db24077ac7ebaa3b640d46dd65dd53e2a3a794d",
    "src/sobol_design.py": "06b16b54b37780ef79e8d5108bbc88d539bdbffb7e4a0b08448a4ac89b382518",
    "src/stage_game.py": "fd480ba426fc43980c66c07715bcd44fedd6f016c5563a4700de8cff7bd36f4e",
    "src/state.py": "7b7784002bd9609fc65bb80296f39dce0f01c202d18e3e8d9823ee6d63fa5854",
    "src/surrogate.py": "640c7950a064bda74e5b330706c3ddfcc435535bd2d191d3e8b3817a40fcdc29",
    "build_exact_dataset.py": "9fe34a5d0ca6b56f69971f60f06b8176390510b4181effd5d8e07e79ff73d6b1",
    "fit_surrogates.py": "04cc2ab81b91f174839d671f3f7ac642f0fffd26c89396a58bf7511ea4248219",
    "run_full_protocol.py": "4390d75a8d3da7f81148a83c40806d70efe8e4abf57ee43f2234939644f43366",
    "search_boundaries.py": "3787805ff8c496baef0fa43a052ff7260553f1a456ac0bf12160e2deab12a714",
    "solve_baseline.py": "a5943c2de718504f8facb6c2967a49aa040922ee94372f0cdc3e6208614551d7"
  },
  "test_files_sha256": {
    "test_bargaining.py": "1d971b3675fb3959e9e3416e43bd2028dcf529be641af19d0fe6bbab04c297c6",
    "test_boundary.py": "bce2a84e71ae45b718afd610187c4e39090124e1b85935204a68dd70c16cad10",
    "test_carbon_tree.py": "051310074601979cff5dd4ea953d6ec9acd0363313bb9f25f0c728f970fbcd31",
    "test_dataset.py": "e6bb76cdc18118d4aa1c474074676c60be6108bb36a21bd556f011271ee76c5d",
    "test_dynamic_solver.py": "cb26277841b9fbd0b5f9a8fa320effafe2a3251642e354862802b90c359d6c37",
    "test_economics.py": "e3d43213d8b15833797beb04d853d35c72241cc45fa9fe36570218fb2aec9f22",
    "test_forward_propagation.py": "fa38333c5b0c00de7ec02e021033d0140088d57b20cfb21d19eeca3e01027d06",
    "test_mixed_nash.py": "3e3dc6c83d4ae4fc83a558604bf95bb9d2ff35454ab415d2b2bce081359dbfc0",
    "test_reproducibility.py": "4dc22a03d6452ab388fc502c36e242ae8b48de06fa2ed4a0aa9f5ae9be7d8494",
    "test_stage_game.py": "f0d73061da0c01d41811c70acb64ae8b8adc10d32cad2f6bfdecc33834830296",
    "test_surrogate.py": "e171b9aca03b85de14ee0fbaa3e0875676b21659c99a1d4c80c9603f406ea54b",
    "test_transactions.py": "920840e7017df8660a1e4a2e01095e626215a9c81b9d4a16c05555e195c72eb7"
  },
  "python": "3.13.9",
  "versions": {
    "numpy": "2.3.5",
    "pandas": "2.3.3",
    "scipy": "1.16.3",
    "scikit-learn": "1.7.2"
  },
  "sobol_seed": 20260921,
  "split_seed": 42,
  "artifacts_sha256": {
    "baseline/baseline_summary.csv": "9192e8c8c35f557a57fe3bcf68b8468d9490bd2c3959a9a17a857705577148fc",
    "baseline/complete.json": "e0941c984c134a4701aa468cab3559e5a7cc15ccca212aa1e67cc19182631308",
    "baseline/JOINT_VENTURE.json": "d34c439371825cc6141dd25d9aba180737408b0c375cdb786a7d124840101e39",
    "baseline/STATE_OWNED.json": "14fe3b57eec41ec2cdfb1ae96318e1f60a6d0d0e7f18c0c42cacaa22b9bc3dda",
    "baseline/TRANSFER.json": "640186d30dfac98651a655b4426a78a71d60166c479d8ac11957a194f6bac866",
    "boundaries/boundary_results.csv": "fc8bf627fc77bd6d9685fe44c40c9adeef06242ad2b850671bbcb9ea4c0d5285",
    "boundaries/response_curves/capex_C_multiplier__JOINT_VENTURE__C_INVEST_PROB_50.csv": "af58238d3dc92b2a724600e3c25ba34c9ef0fec371556264f788620fe18609ac",
    "boundaries/response_curves/capex_C_multiplier__JOINT_VENTURE__SYSTEM_NPV_ZERO.csv": "93d808b2825948ba538e28543b6d9962c8ac8d7146c96cfeab95529241219fb2",
    "boundaries/response_curves/capex_C_multiplier__JOINT_VENTURE__U_INVEST_PROB_50.csv": "af58238d3dc92b2a724600e3c25ba34c9ef0fec371556264f788620fe18609ac",
    "boundaries/response_curves/capex_C_multiplier__STATE_OWNED__C_INVEST_PROB_50.csv": "968642d94da01b1f9cefbea47a1ca938d82646e9fc1a54788f58c14241170fa1",
    "boundaries/response_curves/capex_C_multiplier__STATE_OWNED__SYSTEM_NPV_ZERO.csv": "7beba0c0ca587ccb35eb295d0cbab1cbe1b4c72f3fc00b9b14b9298f249c667b",
    "boundaries/response_curves/capex_C_multiplier__STATE_OWNED__U_INVEST_PROB_50.csv": "968642d94da01b1f9cefbea47a1ca938d82646e9fc1a54788f58c14241170fa1",
    "boundaries/response_curves/capex_C_multiplier__TRANSFER__C_INVEST_PROB_50.csv": "e1a36dd76ad9af147b55405e9ec3fa9b86e3fb1fdf3a263d123d6aa26f8a52e2",
    "boundaries/response_curves/capex_C_multiplier__TRANSFER__SYSTEM_NPV_ZERO.csv": "423fd289d0a52a7b0da412f3318f4d67f5e8e1f6677a83a98d477290c994296c",
    "boundaries/response_curves/capex_C_multiplier__TRANSFER__U_INVEST_PROB_50.csv": "e1a36dd76ad9af147b55405e9ec3fa9b86e3fb1fdf3a263d123d6aa26f8a52e2",
    "boundaries/response_curves/capex_U_multiplier__JOINT_VENTURE__C_INVEST_PROB_50.csv": "83bb7c595a1b335c7caad4211278243320ebf84d7b2327c851d453aa7436aa46",
    "boundaries/response_curves/capex_U_multiplier__JOINT_VENTURE__SYSTEM_NPV_ZERO.csv": "76b020fbd4de191ce1b22a9fe0f775887258dbd943f847bb0cdfc67403d2114e",
    "boundaries/response_curves/capex_U_multiplier__JOINT_VENTURE__U_INVEST_PROB_50.csv": "83bb7c595a1b335c7caad4211278243320ebf84d7b2327c851d453aa7436aa46",
    "boundaries/response_curves/capex_U_multiplier__STATE_OWNED__C_INVEST_PROB_50.csv": "72540d8364cf5ff16c8d7ba7c70019f85ceed3f42409959dcfea3a7b77b8fcd7",
    "boundaries/response_curves/capex_U_multiplier__STATE_OWNED__SYSTEM_NPV_ZERO.csv": "f797144a1f05043869e4bd594dd698176dc222412c61b1144331b92b060b7627",
    "boundaries/response_curves/capex_U_multiplier__STATE_OWNED__U_INVEST_PROB_50.csv": "72540d8364cf5ff16c8d7ba7c70019f85ceed3f42409959dcfea3a7b77b8fcd7",
    "boundaries/response_curves/capex_U_multiplier__TRANSFER__C_INVEST_PROB_50.csv": "6cf70bad2d4e94655e192a194f3bdae126879523f452c74f82d96139e474a5f2",
    "boundaries/response_curves/capex_U_multiplier__TRANSFER__SYSTEM_NPV_ZERO.csv": "f0f0f23f20bcfdfdcb3a1d2994d2a598df993bac9f467ca665b9f6b7d4b5d1c0",
    "boundaries/response_curves/capex_U_multiplier__TRANSFER__U_INVEST_PROB_50.csv": "6cf70bad2d4e94655e192a194f3bdae126879523f452c74f82d96139e474a5f2",
    "boundaries/response_curves/carbon_scale__JOINT_VENTURE__C_INVEST_PROB_50.csv": "a41fd21cd5bbadd172ebdab4d7ec4a7e06d5c63a6e11beb59a32257ca15b5d34",
    "boundaries/response_curves/carbon_scale__JOINT_VENTURE__C_VALUE_ZERO.csv": "4951459f319565456282d676d37228f04650952eb3435f707238d54b260c2331",
    "boundaries/response_curves/carbon_scale__JOINT_VENTURE__CO2_PRICE_ZERO.csv": "b83732e7e827bda7945fcb98d22ae6ce3db8998b314bd1d6f9e1c2866637adea",
    "boundaries/response_curves/carbon_scale__JOINT_VENTURE__SYSTEM_NPV_ZERO.csv": "12615ecd2c8a979738186754dd2d3023ca00d5f6b5967003d4253242b5c19a44",
    "boundaries/response_curves/carbon_scale__JOINT_VENTURE__U_INVEST_PROB_50.csv": "a41fd21cd5bbadd172ebdab4d7ec4a7e06d5c63a6e11beb59a32257ca15b5d34",
    "boundaries/response_curves/carbon_scale__JOINT_VENTURE__U_VALUE_ZERO.csv": "23b6e80a98a98dcd87531ef3b6e7a76c7f9320a48fb9108604f2a4aa73256dea",
    "boundaries/response_curves/carbon_scale__STATE_OWNED__C_INVEST_PROB_50.csv": "4c646d154d16c3407fe4ebb8ec0cf76dea0985c5091604a8a5380c56b4fdd756",
    "boundaries/response_curves/carbon_scale__STATE_OWNED__SYSTEM_NPV_ZERO.csv": "6c49b00e06f10fafd4e3e5640a406b0c6257c973dc552401af0416b407c502eb",
    "boundaries/response_curves/carbon_scale__STATE_OWNED__U_INVEST_PROB_50.csv": "4c646d154d16c3407fe4ebb8ec0cf76dea0985c5091604a8a5380c56b4fdd756",
    "boundaries/response_curves/carbon_scale__TRANSFER__C_INVEST_PROB_50.csv": "a6ae332221d06e08c7a024b70ba326b50e13c7516ea2cc33eef8cd69d887f1a4",
    "boundaries/response_curves/carbon_scale__TRANSFER__C_VALUE_ZERO.csv": "1af117281fb38c2d734e9f128b360736200486d252739bc94640908a1c45db0b",
    "boundaries/response_curves/carbon_scale__TRANSFER__CO2_PRICE_ZERO.csv": "83aa356d29be21d38f8c5cd5a0123148bc2197c8c965901ae6cce8018fc23c8d",
    "boundaries/response_curves/carbon_scale__TRANSFER__STORAGE_FEE_ZERO.csv": "70f8cd4be0e2adcf851f21a59c6b73da47953a034238b644b6a97dafd3a78ed9",
    "boundaries/response_curves/carbon_scale__TRANSFER__SYSTEM_NPV_ZERO.csv": "571add78445249c3bcf5c270cec09961850da8a41650279d11413541839664e5",
    "boundaries/response_curves/carbon_scale__TRANSFER__U_INVEST_PROB_50.csv": "a6ae332221d06e08c7a024b70ba326b50e13c7516ea2cc33eef8cd69d887f1a4",
    "boundaries/response_curves/carbon_scale__TRANSFER__U_VALUE_ZERO.csv": "dbbe278c6c7c8b5f179aa4c99ef24105f61548e79d7dc2195a3d9415d519ff78",
    "boundaries/response_curves/effective_abatement_fraction__JOINT_VENTURE__C_INVEST_PROB_50.csv": "3a80dba3ca8adcc4197943237e47c57dca76df899ebde2b6a91c09f993da57e2",
    "boundaries/response_curves/effective_abatement_fraction__JOINT_VENTURE__SYSTEM_NPV_ZERO.csv": "1e7567d5e79cf6f606af071a945aea883e3910f8bda0797c885d842bbd686ced",
    "boundaries/response_curves/effective_abatement_fraction__JOINT_VENTURE__U_INVEST_PROB_50.csv": "3a80dba3ca8adcc4197943237e47c57dca76df899ebde2b6a91c09f993da57e2",
    "boundaries/response_curves/effective_abatement_fraction__STATE_OWNED__C_INVEST_PROB_50.csv": "719362d682425e6b5481ab44ada2df00fbaa560c32aecaac26ab613229c6d6b5",
    "boundaries/response_curves/effective_abatement_fraction__STATE_OWNED__SYSTEM_NPV_ZERO.csv": "3a58c9b9902d1eec9269d7d9a0d702c8d60176da71d47b3b42784f2e625d5072",
    "boundaries/response_curves/effective_abatement_fraction__STATE_OWNED__U_INVEST_PROB_50.csv": "719362d682425e6b5481ab44ada2df00fbaa560c32aecaac26ab613229c6d6b5",
    "boundaries/response_curves/effective_abatement_fraction__TRANSFER__C_INVEST_PROB_50.csv": "e2e096d10f204daf09f0551b5196d0bc3fb429f1329257d2f34eb59c18b1d7b3",
    "boundaries/response_curves/effective_abatement_fraction__TRANSFER__SYSTEM_NPV_ZERO.csv": "832d4e596c71541747f568331e416a2324605de8a77352df5019acbea47bc757",
    "boundaries/response_curves/effective_abatement_fraction__TRANSFER__U_INVEST_PROB_50.csv": "e2e096d10f204daf09f0551b5196d0bc3fb429f1329257d2f34eb59c18b1d7b3",
    "boundaries/response_curves/storage_subsidy__JOINT_VENTURE__C_INVEST_PROB_50.csv": "7b663b391f9a04f3fc961fa6e04e80b3d69b4715d4b7321d85dcf435cbedd586",
    "boundaries/response_curves/storage_subsidy__JOINT_VENTURE__SYSTEM_NPV_ZERO.csv": "943e67eaa341960fe4d8449922bf66b57180d37a4d4e87f4f6a7d708c872c604",
    "boundaries/response_curves/storage_subsidy__JOINT_VENTURE__U_INVEST_PROB_50.csv": "7b663b391f9a04f3fc961fa6e04e80b3d69b4715d4b7321d85dcf435cbedd586",
    "boundaries/response_curves/storage_subsidy__STATE_OWNED__C_INVEST_PROB_50.csv": "eb506de65a9b5988960e2c3fd521a65d295ce4717a5e71199b6eaab109706a12",
    "boundaries/response_curves/storage_subsidy__STATE_OWNED__SYSTEM_NPV_ZERO.csv": "3c1d877c5da28adee0d5fec4987ad50e944101b465153c4e7b27cae4575947ba",
    "boundaries/response_curves/storage_subsidy__STATE_OWNED__U_INVEST_PROB_50.csv": "eb506de65a9b5988960e2c3fd521a65d295ce4717a5e71199b6eaab109706a12",
    "boundaries/response_curves/storage_subsidy__TRANSFER__C_INVEST_PROB_50.csv": "37a2d86c8084e683eed14b3bfdca9dac37a2f347c6398ab0f769553228aaa1c4",
    "boundaries/response_curves/storage_subsidy__TRANSFER__SYSTEM_NPV_ZERO.csv": "c07b415230ed5f7ca2fe89cf0268fbd2daab81e1bd3ae2c119298318ee070e0e",
    "boundaries/response_curves/storage_subsidy__TRANSFER__U_INVEST_PROB_50.csv": "37a2d86c8084e683eed14b3bfdca9dac37a2f347c6398ab0f769553228aaa1c4",
    "boundaries/response_curves/transport_market_price__JOINT_VENTURE__C_INVEST_PROB_50.csv": "74cda4038387b209de1670d685a100f94c78c5d05f6637ec98f7274a9f98ae98",
    "boundaries/response_curves/transport_market_price__JOINT_VENTURE__SYSTEM_NPV_ZERO.csv": "e129d36108b3904c0fb43cb697ab9a2a072c9ef0b872cdb8fe40eff4554335e6",
    "boundaries/response_curves/transport_market_price__JOINT_VENTURE__U_INVEST_PROB_50.csv": "74cda4038387b209de1670d685a100f94c78c5d05f6637ec98f7274a9f98ae98",
    "boundaries/response_curves/transport_market_price__STATE_OWNED__C_INVEST_PROB_50.csv": "d5f23964b3d81801ea108f4f7ac2f2f559b4c888976b23a4b1e1a0fc487ca442",
    "boundaries/response_curves/transport_market_price__STATE_OWNED__SYSTEM_NPV_ZERO.csv": "71ccc4dd3b6a4b5099dc767dd265481910247b0f525b659a18cfb12037ce3f50",
    "boundaries/response_curves/transport_market_price__STATE_OWNED__U_INVEST_PROB_50.csv": "d5f23964b3d81801ea108f4f7ac2f2f559b4c888976b23a4b1e1a0fc487ca442",
    "boundaries/response_curves/transport_market_price__TRANSFER__C_INVEST_PROB_50.csv": "40a2ac7137b51c189085d91523de21f7c79b3ed6c3d581922e5da7ca375fa0d8",
    "boundaries/response_curves/transport_market_price__TRANSFER__SYSTEM_NPV_ZERO.csv": "8c049095c5a8dfd84fadfaa45ae91193dd4b689ad6752ad029f1c26d34813b38",
    "boundaries/response_curves/transport_market_price__TRANSFER__U_INVEST_PROB_50.csv": "40a2ac7137b51c189085d91523de21f7c79b3ed6c3d581922e5da7ca375fa0d8",
    "boundaries/verification/capex_C_multiplier__JOINT_VENTURE__C_INVEST_PROB_50.json": "fd959e338644bbd5b356c062ba192d7cc6d642c2cff422b58083a936b14c7469",
    "boundaries/verification/capex_C_multiplier__JOINT_VENTURE__SYSTEM_NPV_ZERO.json": "1075d27c733d9ed4f8b7b7380c4c7131d0cf4571ab4dd1e06024cb783527b26a",
    "boundaries/verification/capex_C_multiplier__JOINT_VENTURE__U_INVEST_PROB_50.json": "0ac778ff83dc92d10279154d4ff46e0ce872bf6e1d52c933edd32e39a4af9d54",
    "boundaries/verification/capex_C_multiplier__STATE_OWNED__C_INVEST_PROB_50.json": "f6d74116765c0947d9e481fb9b459d7014aeebfb012b8d8c542cf542a2af9ac9",
    "boundaries/verification/capex_C_multiplier__STATE_OWNED__SYSTEM_NPV_ZERO.json": "e3d0db876f0d1c0c790a4ccc5dbf4789562fcfaab7ec99189b537ba20b418534",
    "boundaries/verification/capex_C_multiplier__STATE_OWNED__U_INVEST_PROB_50.json": "4413f38144b17cb753ae757ce829880d2f205a10c7c3c2a52e86f39aa9ddd9cc",
    "boundaries/verification/capex_C_multiplier__TRANSFER__C_INVEST_PROB_50.json": "c77790f37a3cf527f7e596af4b14da200e7f25ae144ca165c432747351376704",
    "boundaries/verification/capex_C_multiplier__TRANSFER__SYSTEM_NPV_ZERO.json": "86a1d2c81262458f419d10e53c7f698f076354174e2aff09997d8b2ab3269685",
    "boundaries/verification/capex_C_multiplier__TRANSFER__U_INVEST_PROB_50.json": "3899a220d51ac12ade4f0f21af5a17101240475c1143dbc2ff30b8e247243fdb",
    "boundaries/verification/capex_U_multiplier__JOINT_VENTURE__C_INVEST_PROB_50.json": "e349188116d9971528569c8e2790ae1748509bd1641c7723f6b4907a8905b656",
    "boundaries/verification/capex_U_multiplier__JOINT_VENTURE__SYSTEM_NPV_ZERO.json": "3cedd043f995f82367df9bebddda783c901aa41787b6891e3bc2c018d8e508f4",
    "boundaries/verification/capex_U_multiplier__JOINT_VENTURE__U_INVEST_PROB_50.json": "62c4a54c98729bc99afe512e069ce44d8f7e0e23ce2e944c504a6a6df496d05b",
    "boundaries/verification/capex_U_multiplier__STATE_OWNED__C_INVEST_PROB_50.json": "4d09a20394fe1969f6da29f7468e250d78737ec9c2f55b39eec987d93d734322",
    "boundaries/verification/capex_U_multiplier__STATE_OWNED__SYSTEM_NPV_ZERO.json": "443c713d42535add1a25bedd1566af16b21644ac4d26e5373e18c949ab215e1c",
    "boundaries/verification/capex_U_multiplier__STATE_OWNED__U_INVEST_PROB_50.json": "2f1e8cece4d3bd2f94b5934d0a295898caba2b9d33c58aca6f4d9413a09eb009",
    "boundaries/verification/capex_U_multiplier__TRANSFER__C_INVEST_PROB_50.json": "812c2339ddf119b951c340796cb3dd7c7b53afa64bc1c8977743a9c6ca6664bf",
    "boundaries/verification/capex_U_multiplier__TRANSFER__SYSTEM_NPV_ZERO.json": "113f80e273e983347342534dad68bec3956e7d80b04fe0e150772d9a3a087a28",
    "boundaries/verification/capex_U_multiplier__TRANSFER__U_INVEST_PROB_50.json": "a9b9838ed1f4f7396f082f63683c205c05a6313e977a6b70098a36aa96b568a6",
    "boundaries/verification/carbon_scale__JOINT_VENTURE__C_INVEST_PROB_50.json": "ae001357d603dca7e057df150aaf20bf26afdc39995888bb1b0054a890cf0f6f",
    "boundaries/verification/carbon_scale__JOINT_VENTURE__C_VALUE_ZERO.json": "7f4316c9afc4fb81ca38dcad96fd154d2c9a5cbe1d4f8a18ff13692cd3eff81d",
    "boundaries/verification/carbon_scale__JOINT_VENTURE__CO2_PRICE_ZERO.json": "4ae16e3b8fc698f147c7d14ec742ee44530bb708fa4b588288c2f7db6af62270",
    "boundaries/verification/carbon_scale__JOINT_VENTURE__SYSTEM_NPV_ZERO.json": "7b5e7be07cbd8095512f1e0f3441b7a17990af5fdd47691a281900c528fa3e04",
    "boundaries/verification/carbon_scale__JOINT_VENTURE__U_INVEST_PROB_50.json": "d68f72c46f7ebefb858e092e865b9ab99d6a3c83c42415eca5687186420b38ca",
    "boundaries/verification/carbon_scale__JOINT_VENTURE__U_VALUE_ZERO.json": "5219c9e941c29f75aca4c17f6a266b1c960ae62402df18fb0e57f80a9988fc56",
    "boundaries/verification/carbon_scale__STATE_OWNED__C_INVEST_PROB_50.json": "c52f63a4de59b19e83bd3d8a43f86fa431c7da14e727104b7725bc6722825ed4",
    "boundaries/verification/carbon_scale__STATE_OWNED__SYSTEM_NPV_ZERO.json": "9ecaf418124b4a44bf6958f6bbdda3b7dd0f05694aaea38a398d964e52ff857e",
    "boundaries/verification/carbon_scale__STATE_OWNED__U_INVEST_PROB_50.json": "7a7bf93f5608d6e15b94e0959bf14854445e2cb54e63c7716682ccab7f451f02",
    "boundaries/verification/carbon_scale__TRANSFER__C_INVEST_PROB_50.json": "8e5432e7b2e3740daa7c0701a6686a8eb791bfd4c457fa56183fd979a23f0d5a",
    "boundaries/verification/carbon_scale__TRANSFER__C_VALUE_ZERO.json": "ebca0e58b60fadfbc5711fa68d226afd951d12e984b4909417e82a532111c2c9",
    "boundaries/verification/carbon_scale__TRANSFER__CO2_PRICE_ZERO.json": "9196fcbc6e429ea4bf0165bcb94edc7ccb396284361f40bf508829b498048219",
    "boundaries/verification/carbon_scale__TRANSFER__STORAGE_FEE_ZERO.json": "d3467609133fdbf1082525aa1fc5ab0d40790c79ad1abe0ec0f8d02666095cbc",
    "boundaries/verification/carbon_scale__TRANSFER__SYSTEM_NPV_ZERO.json": "d95a57ec0b7d177043903350fa89ee7464ae809b122a614508956dab3a0032bb",
    "boundaries/verification/carbon_scale__TRANSFER__U_INVEST_PROB_50.json": "2cab267ad849f86ad31d345a2eb139fb65412459457efbd1b907377a5facb020",
    "boundaries/verification/carbon_scale__TRANSFER__U_VALUE_ZERO.json": "83a45a18a26488bb34ef3a5aab17f3d6499c61b0f443fa62d1ab5955862759ab",
    "boundaries/verification/effective_abatement_fraction__JOINT_VENTURE__C_INVEST_PROB_50.json": "7662af4f5216cab59340058301b8dbdc5034aeb69cf2cb73203a402b718c5710",
    "boundaries/verification/effective_abatement_fraction__JOINT_VENTURE__SYSTEM_NPV_ZERO.json": "979036b8043e35309cb534e7dd87d0bf356215b29fb61651de4bd33adf77ab31",
    "boundaries/verification/effective_abatement_fraction__JOINT_VENTURE__U_INVEST_PROB_50.json": "4f689143b137e9009de229c4ed300154f6d79c0bcf3b3a0657a807f7e13aebc0",
    "boundaries/verification/effective_abatement_fraction__STATE_OWNED__C_INVEST_PROB_50.json": "0e073945655d067582042de64d9b87d33fdf40f2b21a76d6f51e2bad550b0c17",
    "boundaries/verification/effective_abatement_fraction__STATE_OWNED__SYSTEM_NPV_ZERO.json": "da87f4889e45ea3ea49020fd564fb5b087e2669ff2b88e190076c9216c48bd7b",
    "boundaries/verification/effective_abatement_fraction__STATE_OWNED__U_INVEST_PROB_50.json": "d319902fc903081ca041a351968b8fdcaf5fb88db4d9c29432865f2671642699",
    "boundaries/verification/effective_abatement_fraction__TRANSFER__C_INVEST_PROB_50.json": "ff8efebdfe184af1de28fa05529ea95643946dbcdbe9d4013b92bc189370f9fb",
    "boundaries/verification/effective_abatement_fraction__TRANSFER__SYSTEM_NPV_ZERO.json": "fb8a0ad623dfb0b48ee848b6333a28635febf940cd279dbc4f9f2d61827f4990",
    "boundaries/verification/effective_abatement_fraction__TRANSFER__U_INVEST_PROB_50.json": "2e2555ddcc340e658d9dae42f1e33ffc6158695e4529296f0ac6bf240199ff42",
    "boundaries/verification/storage_subsidy__JOINT_VENTURE__C_INVEST_PROB_50.json": "ea54ecbb747a76d245a7ada6ef515e1658ecf4a62fe09b1b3ed89be65b3688a4",
    "boundaries/verification/storage_subsidy__JOINT_VENTURE__SYSTEM_NPV_ZERO.json": "2e833ee4d7456dcb459c5b1fe4bdc285c55badb90b40c2c2589724ab3bffa82b",
    "boundaries/verification/storage_subsidy__JOINT_VENTURE__U_INVEST_PROB_50.json": "96883895fe121f138536ac0a59e4ecc1f52a9870ccdaafb34a5fe85a4f6ab891",
    "boundaries/verification/storage_subsidy__STATE_OWNED__C_INVEST_PROB_50.json": "ecbb5447056a9a056764a11274f2fa17d1b994f7a55badca6e8c4e5e774a1222",
    "boundaries/verification/storage_subsidy__STATE_OWNED__SYSTEM_NPV_ZERO.json": "0f4fda9b10093a18a4ae1a7443dc954f8a8ac4c2bb1bf83a51265b0f66728c20",
    "boundaries/verification/storage_subsidy__STATE_OWNED__U_INVEST_PROB_50.json": "c7b4617dceec50f73d891f5386426cfdd50c739982eb49eb4422b9d3235c7448",
    "boundaries/verification/storage_subsidy__TRANSFER__C_INVEST_PROB_50.json": "6922cbeb90f0ab396b8350feca4429280f8459a14405763f35cde1ee79a0cf61",
    "boundaries/verification/storage_subsidy__TRANSFER__SYSTEM_NPV_ZERO.json": "899c6bbef07fcea79dd55130d72acf374e9f51a1bd0aa0e3936a19a2206f22a9",
    "boundaries/verification/storage_subsidy__TRANSFER__U_INVEST_PROB_50.json": "9f5e6ef459c9e081b835838d553b932ef72e46e7fb772facaca50c16d3cd8738",
    "boundaries/verification/transport_market_price__JOINT_VENTURE__C_INVEST_PROB_50.json": "cce43f0f21543f07c9077100986b659736868837b1c8e811d8fe4f13a9ad50a1",
    "boundaries/verification/transport_market_price__JOINT_VENTURE__SYSTEM_NPV_ZERO.json": "a0f0f0a417eced6d5ae08cb49a01fde12659ff0e1fbe10528e377a32fa1518cb",
    "boundaries/verification/transport_market_price__JOINT_VENTURE__U_INVEST_PROB_50.json": "bc3f6b500e7bdfb934e7a3a879dcc02f831a717e2cbb70ddf473916863448ba7",
    "boundaries/verification/transport_market_price__STATE_OWNED__C_INVEST_PROB_50.json": "7017e5eec588128ec2719e51a0159b6e6a035a4b8a70ca023c81e71caa55233b",
    "boundaries/verification/transport_market_price__STATE_OWNED__SYSTEM_NPV_ZERO.json": "611c11f0f36868b0a23d38882eddb2a1ac49b56f9ad003ca84bbc64f09d046d7",
    "boundaries/verification/transport_market_price__STATE_OWNED__U_INVEST_PROB_50.json": "edf0de38b282dee4e5dc51fe61d8eef3c400612f41c86b9aea3b8a2ff8c8e2ae",
    "boundaries/verification/transport_market_price__TRANSFER__C_INVEST_PROB_50.json": "1c41ef21fbd0df1248ccb1d9625bd639d8ee08f7f7cea2714d25b18eed1b63ab",
    "boundaries/verification/transport_market_price__TRANSFER__SYSTEM_NPV_ZERO.json": "2061db72ba2a70f05258be598d8bd6978106d06706df701609b195dfb05286c7",
    "boundaries/verification/transport_market_price__TRANSFER__U_INVEST_PROB_50.json": "01827330f531ca3f880b8985246f845bf6fc224396b7f58f3ceea127ac63d42b",
    "exact_dataset/chunks/chunk_0000.json": "7c09b6f229671fd3d3ca5e254c593c61d99f5366fcee22039dad385215b87128",
    "exact_dataset/chunks/chunk_0000.parquet": "75d61f4ac9037b50128719ff26c7c66045c126cf9119e1da9a60f3516ca49072",
    "exact_dataset/chunks/chunk_0001.json": "af6d00ba27f74f1b6d40424c8e4cab9edb876a40aaa73f5e3b05a7f29cf8c0b5",
    "exact_dataset/chunks/chunk_0001.parquet": "a135436461e50316afb71f1755eb792cefdd3d68656e6aebecf13158aa1161cb",
    "exact_dataset/chunks/chunk_0002.json": "9acc9859f08ae6aa1024620a3d80681b5a1e3f59de2bc8bafb099fe73fa81484",
    "exact_dataset/chunks/chunk_0002.parquet": "d3a754009c584a1cdb8288089efe73d90667592653b9afa8348181e4265979ad",
    "exact_dataset/chunks/chunk_0003.json": "54b495cc70c89d3443b7f436748e5cf5d682e896951968c2c54d211bd1fbdd13",
    "exact_dataset/chunks/chunk_0003.parquet": "52fcd80fc911ab7011bdcc71dc8b6159bdbf76d93ce86ad7d8ecb0ddaec4691a",
    "exact_dataset/chunks/chunk_0004.json": "a37d456006e10c2ae6f607677aefa1caa7f36c1c8720cc7a25811fb573b19e7f",
    "exact_dataset/chunks/chunk_0004.parquet": "340c574350eb5f7cf01dc9ec6bc322e77d02c4ff58771ca03c2e29cc487375d2",
    "exact_dataset/chunks/chunk_0005.json": "be22a64d9238d945abb3b1ebe58e232a9cbf560c76ab6d2b12b5cc580b6dd0fc",
    "exact_dataset/chunks/chunk_0005.parquet": "04a9e671dbf857fa380828e5206a58e6fd76f5950f4b4ed7921c5fffbc175723",
    "exact_dataset/chunks/chunk_0006.json": "3398ea615e4dcf7a42b9efdec0b20f0c44ab4ea8a7585cdccdc9498fc5dfc10c",
    "exact_dataset/chunks/chunk_0006.parquet": "a183071fdfaaa6d5c4aa8a85a2516c3816194ba20f397faa3cdc3f1b4ddcbec1",
    "exact_dataset/chunks/chunk_0007.json": "eecf8c2fa19026ce33c1f356ca9022ad36857d2d2cd9b171f33f2368d75bb25a",
    "exact_dataset/chunks/chunk_0007.parquet": "b505d4847b010713ca19439bf80448c82905d91b2375f4096d82dfad89222688",
    "exact_dataset/chunks/chunk_0008.json": "5c0b2a16dd8dbeadfd998933a6bf8aaa4b542d1904c816735100b20e64e0ca2c",
    "exact_dataset/chunks/chunk_0008.parquet": "a33ed3d90d8a4dbd3290cdc4aeb67fd3ac5da9db499260383f3635cb488fb2a8",
    "exact_dataset/chunks/chunk_0009.json": "ac99481f6e742bdd6d0390e22c960e35e35f979cbfae0d69150da43c4f3311fb",
    "exact_dataset/chunks/chunk_0009.parquet": "a41b7d7c54cfcec9ad140f81e6fc5adc5232ca8cab6a1afc9b6d5521eee00a99",
    "exact_dataset/chunks/chunk_0010.json": "53f035e279022fc4f98945a86f0dee8f826ffb26d8386f0510bad6dc828e1010",
    "exact_dataset/chunks/chunk_0010.parquet": "5daa76a77c3449a1afe9b143c804513e2dfcf0a6f86d0bf05b915840eb022295",
    "exact_dataset/chunks/chunk_0011.json": "a863dc87ca5baecc02390441b56dc52951d02e1fa0b23d7856ae27bc971820f5",
    "exact_dataset/chunks/chunk_0011.parquet": "368532e1785bbebb15a1d2bbb8f56ad1432c1809ae9fd4e87add0d990f65fda3",
    "exact_dataset/chunks/chunk_0012.json": "69b687992697342d096ff15f3e377d53c40e6f8f6c0bc413df5c1d97aa09ca3b",
    "exact_dataset/chunks/chunk_0012.parquet": "1d5df4a6c9cc33ae7558c6a9e7670bfcacfe2d30849042ab5a362d7659750c9e",
    "exact_dataset/chunks/chunk_0013.json": "f61cb2597ab74aab6618e9fdf1807aa78bd63e9b4df919722b80c3f0977c2da9",
    "exact_dataset/chunks/chunk_0013.parquet": "d10d6caf16d9be373b63f2091fb3ca9e2770970e3ad87416c7c138d106a01bd6",
    "exact_dataset/chunks/chunk_0014.json": "d09023bc8152603402f5c6db570ee32d6f1c10a1e42558798ebba69e54987076",
    "exact_dataset/chunks/chunk_0014.parquet": "69873989458891150f9ed0ff3d1d995f47113a91cfef3c8be67d667e83f2c879",
    "exact_dataset/chunks/chunk_0015.json": "d80dcd6ef90679fe50ddfb80c783fc809fb6058b8323e05341af177ff9ea2584",
    "exact_dataset/chunks/chunk_0015.parquet": "51851c54ebebdd1ac4f93e8a08c70dcd2b4881209ce20ea402b6ef7ab5c4e246",
    "exact_dataset/chunks/chunk_0016.json": "c30fe1fdbe42da36902596436a5bd58bcbff872cf76cc9da0ef64c7591e4ebc9",
    "exact_dataset/chunks/chunk_0016.parquet": "f31c398f3ae20935b0a19226d3b79ea1b0c04e4208bfd1b624e288fde0e0c5cf",
    "exact_dataset/chunks/chunk_0017.json": "47ce18e3cef714f1d38d0ee2d605cbd319365aa5df4925f19dca8cb851cb8f41",
    "exact_dataset/chunks/chunk_0017.parquet": "659e72a3c8b90835a466129a00072d2dd1a691b89b6b1120e68b827908dbde62",
    "exact_dataset/chunks/chunk_0018.json": "cb8006288bc3c2e063a0fcc685edff66fe524344f04a393807db0329ca27fb71",
    "exact_dataset/chunks/chunk_0018.parquet": "f04e37dff707e0e27fa945252730cc8a65e5b62d3b1337584ae510177e32e1c9",
    "exact_dataset/chunks/chunk_0019.json": "7f6220ca2113a411d3e3a47e78e7a9d1c750465f6440692266c140d554685691",
    "exact_dataset/chunks/chunk_0019.parquet": "1dbf91e2fe91dd52f87d5b913dcd1bbef8993c38a1d6426dc759e83e22bb2def",
    "exact_dataset/chunks/chunk_0020.json": "7c5572deef1103d54a915eb0ce7e5e5cb3c397ad0ad45f28d38a2ed104a5dac3",
    "exact_dataset/chunks/chunk_0020.parquet": "542bbb2f0cf537cb4d401808daa8fb49bd01100e3d170336d494c0c462319cbc",
    "exact_dataset/chunks/chunk_0021.json": "f2934c92176a34e5d65d6b0439bcf057cfa13dab8d2b922190b4fd0c6c444430",
    "exact_dataset/chunks/chunk_0021.parquet": "9180cb3626824fd4b2bac87b137626f484e325f0fd77af1f4383f650d35ba07f",
    "exact_dataset/chunks/chunk_0022.json": "537a6eede92c59f4479673b0847bbd6874b6131343e9b6c59a15f7b4eb3d6459",
    "exact_dataset/chunks/chunk_0022.parquet": "482749a7e460fe84fa8c3d166da64d7e93bf82221ad179b4a30c64dff525cd01",
    "exact_dataset/chunks/chunk_0023.json": "d3fb2ee062da245028286d4e078a4e0564dce6745e9cf4984675f9ae396eafaa",
    "exact_dataset/chunks/chunk_0023.parquet": "508baecbd080d11aff4d3b56f1e4cf6cd29aaf306b6deac422696f3cad14645a",
    "exact_dataset/chunks/chunk_0024.json": "76eb9553009ff72c7efda1137d2164efa207868f14548c5ca2f33b7d66c7a65c",
    "exact_dataset/chunks/chunk_0024.parquet": "67140f83f09c19a854e08000b2fbbdad819b0d41af51edcf315c6584697aba11",
    "exact_dataset/chunks/chunk_0025.json": "bacfbcf238677347d43a06154e0ca4254e9c29b5594c7166e027af138279bd39",
    "exact_dataset/chunks/chunk_0025.parquet": "0092b81590cfd50f23e156e1cf88cd05eb97d8deb558c2092a56ab3951549da0",
    "exact_dataset/chunks/chunk_0026.json": "1d3732552a3c6774102658dd6a0db0271700398e9bfa12304ca29996c2856230",
    "exact_dataset/chunks/chunk_0026.parquet": "b0cf2762c8a72035eeb43b4e87e4115218729ade190252385b5efecefa8b879e",
    "exact_dataset/chunks/chunk_0027.json": "d46fbb2f4df89d509461b53abb0419a58c4afa7960dcb1d31c686da4b411aafb",
    "exact_dataset/chunks/chunk_0027.parquet": "df94a16636af47aeb711ec0f3c986bbdbc933ef19b6adf4d9627f584b3760396",
    "exact_dataset/chunks/chunk_0028.json": "16b519d0db9f50efdd96bbfce2862a7ff0976b6f6688e4bdaccd3fb90b2268f3",
    "exact_dataset/chunks/chunk_0028.parquet": "9968b51c19fef00e88b1e783ff977e71034ad32cb271423193ff89f6b451c6bd",
    "exact_dataset/chunks/chunk_0029.json": "54ec3c87fd224981e1091cc50f2ab1b92e523829e0445fecdc3e33eae1930c25",
    "exact_dataset/chunks/chunk_0029.parquet": "bd9d953f82e6f5cbf64d8407a2f9978911d767c2f0ed3f3b5fa78019668e20ff",
    "exact_dataset/chunks/chunk_0030.json": "4c3b3bdedd3175846cb83c3ab1aec793a7f736063a192f51008e5030404b611d",
    "exact_dataset/chunks/chunk_0030.parquet": "66783c575723f8d7dcf033a52cec9eebb038ee3c274006329ba040ff07a9f4bb",
    "exact_dataset/chunks/chunk_0031.json": "7179074b2a17e4739b352e2d77b0af8890a77bcfae6f65f7d9078b4c6d5ed341",
    "exact_dataset/chunks/chunk_0031.parquet": "819a8b50ce19c78e0bddcfba75e9633b9c925325e16e41eb962f66df4d6de2fb",
    "exact_dataset/exact_equilibrium_outputs.csv": "e827973c6e1e1463df4e92c2b3a9257303129cc49c004adae90f94e25882d232",
    "exact_dataset/exact_scenarios.csv": "715a395fa9944def62d77f9c1ebe348213a2741bdd3507f22331d11df426f6e8",
    "final_validation.json": "01a3b3692a399963aea49cad63a045f84cdd01169b0d2c7c8fc16bb836863fb9",
    "formal_run_lock.json": "c5013887c33cc8869f204036574dd7995b7ea34835ac94e6c6c9eabe0776607a",
    "gates/gate_1_COMPILE_TESTS_CONFIG.json": "bbed41279fdb1f72af21735d36607ee076aa22c11b0d8252ab216fea23c7d794",
    "gates/gate_2_BASELINE.json": "6339a8ef3ac6cf50f0c3b314e22063c3af9dac0c447767672017501ec1f0d3ea",
    "gates/gate_3_EXACT_DATASET.json": "b4600ea2f409d1703c164649297b34080a2ce4e011fbc15598cf2ff637b0b99b",
    "gates/gate_4_EXACT_INTEGRITY.json": "b4baa37a86bdf74f28f7ebdc2551065aaaaba965fc534f06232cd6ad86fb424e",
    "gates/gate_5_SURROGATE_FIT.json": "f48fe375592c19940893b694ef4252b57ceffdd2dcdeb518183b04a19471f6ee",
    "gates/gate_6_SURROGATE_ACCURACY.json": "0a0f5e75e952dc8c4db9f30be4ee2a4db5c879d14ceccadba93f55e5dc395310",
    "gates/gate_7_EXACT_VERIFIED_BOUNDARIES.json": "601ed5c2e8c20dede7228a6779a70316872c02fe34e044a23358bedec2122f13",
    "precheck.json": "5180e3984565bffc1b891c14d76f83cba91a6fbf1a906544c5c4c3539d148e0b",
    "surrogate/models/JOINT_VENTURE__expected_tau_C_conditional.joblib": "9c4d3deaf86b2c2c68d5494602f92dff99639caf3e2ed697c0a2c41599ce3176",
    "surrogate/models/JOINT_VENTURE__expected_tau_C_conditional.json": "9a4adda732205c1cb75015581cdf66c7eb61ef255490d83d8f5258b469bd800a",
    "surrogate/models/JOINT_VENTURE__expected_tau_U_conditional.joblib": "9c4d3deaf86b2c2c68d5494602f92dff99639caf3e2ed697c0a2c41599ce3176",
    "surrogate/models/JOINT_VENTURE__expected_tau_U_conditional.json": "8c9d7373e9f2ab4a15910b706bdbe3963bbd89329fbb836ec1ee248fcac324f8",
    "surrogate/models/JOINT_VENTURE__invest_prob_C.joblib": "d7005efb5cee1b88ab978062520087e3723a62b05ccbcd634ad18011391e915f",
    "surrogate/models/JOINT_VENTURE__invest_prob_C.json": "d019f0571ca5d7c82720497806413d66b250dc5e6a52f39bdd52500c5bd2c7bf",
    "surrogate/models/JOINT_VENTURE__invest_prob_U.joblib": "d7005efb5cee1b88ab978062520087e3723a62b05ccbcd634ad18011391e915f",
    "surrogate/models/JOINT_VENTURE__invest_prob_U.json": "225c87c58ed05cbfc930c021c8e80a283bdb2ec36a7d3448819e3fdb584f3c97",
    "surrogate/models/JOINT_VENTURE__mean_co2_price_conditional.joblib": "55a60abf87010fb6d0f5f992ded8bffc704c6cc3d8f9925a054c636f5ab14565",
    "surrogate/models/JOINT_VENTURE__mean_co2_price_conditional.json": "1e9a940dc9385e1b5b9dc442d9806c1d54c0ebb514d37c61b1df2b823bf60bc1",
    "surrogate/models/JOINT_VENTURE__system_npv.joblib": "177a9651abb106cc41de6db9b7c38fcd62f34e60d39805987aeb4593d5a3c31c",
    "surrogate/models/JOINT_VENTURE__system_npv.json": "0c0178ffc9a5eb5ef28559b9b25c5c0c9f635fa87a0e1a78f1c084e73c120e9d",
    "surrogate/models/JOINT_VENTURE__value_C.joblib": "80f8f4649d0c1c4637172e009f8a8c1b95da83107de8869c6b0693476067a3ad",
    "surrogate/models/JOINT_VENTURE__value_C.json": "3997e1387f5044c18704f855f6ea6e74d49bd1648ebaa39ebca314bd2d2c6e3c",
    "surrogate/models/JOINT_VENTURE__value_T.joblib": "c9503beec54a7b44656aeab57ddf6a4c55d2cf587206d606c00884fd7f914a95",
    "surrogate/models/JOINT_VENTURE__value_T.json": "d144cd923e7128f7b0c43461e8fb9fd56cc36e164067dd33baa533536ebc400f",
    "surrogate/models/JOINT_VENTURE__value_U.joblib": "7f4b97f74b44efdc6e58e0a5fbc3e05595e90664c80cd412a6650b25ca977f5a",
    "surrogate/models/JOINT_VENTURE__value_U.json": "7ecfd6a00dda313f27ed967aa8d4eec23e4d6b3ea5fe4547014753f34e1da8b8",
    "surrogate/models/STATE_OWNED__expected_tau_C_conditional.joblib": "96ad5292ee7968ed1cbf03af7569e3376991dc9faf683f373ef26fdb41851f8f",
    "surrogate/models/STATE_OWNED__expected_tau_C_conditional.json": "e8e911d565c889e4a3cc4b277d57b49fbab89b209d935a29b6b3cfc6c8bc91d2",
    "surrogate/models/STATE_OWNED__expected_tau_U_conditional.joblib": "96ad5292ee7968ed1cbf03af7569e3376991dc9faf683f373ef26fdb41851f8f",
    "surrogate/models/STATE_OWNED__expected_tau_U_conditional.json": "5d65f09b6ac327afaa2077af2480ed5a56371ae7c45fe9369eac1c2630618e31",
    "surrogate/models/STATE_OWNED__invest_prob_C.joblib": "9544553a5fb165f4029228ba94036e63d9431acaa886254955c7e269501fad22",
    "surrogate/models/STATE_OWNED__invest_prob_C.json": "3847cabf5e553a12d351c88b8f4ab1607aaf4f78c0e57c10e31ca626d36e99bc",
    "surrogate/models/STATE_OWNED__invest_prob_U.joblib": "9544553a5fb165f4029228ba94036e63d9431acaa886254955c7e269501fad22",
    "surrogate/models/STATE_OWNED__invest_prob_U.json": "fed8d451bd526638e53615fe573c98eee543095a1b57c8649b55577feef30777",
    "surrogate/models/STATE_OWNED__system_npv.joblib": "3ff2d9b5030f78d01f053efcc6e2fecd80e630b23d18e10983e6011a95331ee5",
    "surrogate/models/STATE_OWNED__system_npv.json": "7d553ca2158d933e2e318460637b403cbfa87eb73074348a805931f41e259e8b",
    "surrogate/models/TRANSFER__expected_tau_C_conditional.joblib": "91cc46f0a131f7cfb00ccdb43a35b79b000db115958f1ff50895da8eec4fde6c",
    "surrogate/models/TRANSFER__expected_tau_C_conditional.json": "37ddeaf93f529ddc14c93bffa123ef4e1ad4555297de0e6826d86093a0ac8cdc",
    "surrogate/models/TRANSFER__expected_tau_U_conditional.joblib": "91cc46f0a131f7cfb00ccdb43a35b79b000db115958f1ff50895da8eec4fde6c",
    "surrogate/models/TRANSFER__expected_tau_U_conditional.json": "def0e0c18417067810b77b27398412096081d60f80a8c44d0dffcc4154cbb54d",
    "surrogate/models/TRANSFER__invest_prob_C.joblib": "1ef839b373fd8ac00d8e5645ea7de6a6e00cf4539d3603d5d8834a4b31a0e65f",
    "surrogate/models/TRANSFER__invest_prob_C.json": "e85dd3569a07ec01b533854f03aaaf0e506a38686c00564ab5186599cb69641c",
    "surrogate/models/TRANSFER__invest_prob_U.joblib": "1ef839b373fd8ac00d8e5645ea7de6a6e00cf4539d3603d5d8834a4b31a0e65f",
    "surrogate/models/TRANSFER__invest_prob_U.json": "125bcc74ee2d22e877b5432ddf0eb7af5db34312d3c43a0ed80a8f8666a8e747",
    "surrogate/models/TRANSFER__mean_co2_price_conditional.joblib": "5611218c81492dd66ff56440a863ba91f3198a0e1551e3ad8a81a87fbd1c16ca",
    "surrogate/models/TRANSFER__mean_co2_price_conditional.json": "96c4ea10dc6aeafc796e5e38b0320d794574f31962415d4a0850aa93290d5a77",
    "surrogate/models/TRANSFER__mean_storage_fee_conditional.joblib": "c8731190249bc65264860afa859ade0b6804e64e74ca9391699f283481145623",
    "surrogate/models/TRANSFER__mean_storage_fee_conditional.json": "85771518257fa34d280890dd821a782e14ba6813f9e0f91bb4845d35ce6f9298",
    "surrogate/models/TRANSFER__system_npv.joblib": "fe69c3a4dc7472b09af077bd097292cfb2d4e2e5cd7d1a6aaa11d01cdd931072",
    "surrogate/models/TRANSFER__system_npv.json": "b6941b46a2780885c7d65d8eaf5fc2857b523407f474c85267f15916871d518f",
    "surrogate/models/TRANSFER__value_C.joblib": "d553d0571fbcef9aceee9485deecb680637a0a48cb2b9ce3704184639b61680b",
    "surrogate/models/TRANSFER__value_C.json": "4b576c03e03d290fa00f08f27893e1686e1a54454c2e0f668c257b41cf3c21e0",
    "surrogate/models/TRANSFER__value_T.joblib": "80b27f7a4b496003eb3d58f4a0de9bc2f3768e6a1dc3bff7ac4703a0bd3ec4f6",
    "surrogate/models/TRANSFER__value_T.json": "61307dde4839a3a478c0299fbbc17d4b57e317b55379f9c71e0a24c8f42ee0c4",
    "surrogate/models/TRANSFER__value_U.joblib": "9163fb5bf44d90404203d62765cf6c7451b79949f6379fe3a3e7f61decb6d1db",
    "surrogate/models/TRANSFER__value_U.json": "0b01d77421c6da8f32621f909b924a0c2663e47b4c941a7ee4aa646f48b7a9b4",
    "surrogate/scenario_split.csv": "2f17364f45b652200c9360d4d78fb27cd2239a02a78b851ff34a9cb0f6f8bb52",
    "surrogate/surrogate_metrics.csv": "8578abf7138747b6c994330d93b91fcf81e8559c190b4cf30e7e2b16efe667d8"
  }
}
```

## Compile and tests

```json
{
  "compileall": {
    "exit_code": 0,
    "stdout": "",
    "stderr": ""
  },
  "pytest": {
    "exit_code": 0,
    "stdout": ".....................................................                    [100%]\n53 passed in 2.02s\n",
    "stderr": ""
  }
}
```

## Baseline three-mode results

```text
 system_npv  value_C  value_U  value_T  expected_active_years  expected_total_quantity  expected_total_utilization  expected_total_storage  max_static_accounting_error  max_backward_forward_value_error  max_probability_mass_error  invest_prob_C  never_invest_prob_C  expected_tau_C_conditional  invest_prob_U  never_invest_prob_U  expected_tau_U_conditional  co2_trade_year_probability  storage_trade_year_probability  mean_co2_price_conditional  mean_storage_fee_conditional  mixed_equilibrium_state_probability  multiple_pure_equilibrium_state_probability  expected_mixed_equilibrium_years  expected_multiple_pure_equilibrium_years          mode  transport_market_price  effective_abatement_fraction  storage_subsidy  capex_C_multiplier  capex_U_multiplier  carbon_scale solver_status initial_equilibrium_type
   5.218776 1.313861 3.904915 0.000000               0.266599                 0.113970                    0.026660                0.087310                 4.547474e-13                      2.220446e-16                4.440892e-16       0.026141             0.973859                   18.801348       0.026141             0.973859                   18.801348                    0.008887                        0.007276                  195.424411                    202.457256                                  0.0                                     0.000871                               0.0                                  0.026141      TRANSFER                   125.0                           0.7              0.0                 1.0                 1.0           1.0            OK                PURE_NASH
   6.126641 1.556499 3.947543 0.622599               0.413907                 0.206953                    0.041391                0.165563                 4.547474e-13                      2.220446e-15                2.220446e-16       0.047182             0.952818                   20.227509       0.047182             0.952818                   20.227509                    0.013797                             NaN                  213.619044                           NaN                                  0.0                                     0.001573                               0.0                                  0.047182 JOINT_VENTURE                   125.0                           0.7              0.0                 1.0                 1.0           1.0            OK                PURE_NASH
   6.653657 6.653657 6.653657      NaN               0.711803                 0.355901                    0.071180                0.284721                 5.684342e-14                      1.776357e-15                2.220446e-16       0.069652             0.930348                   18.780532       0.069652             0.930348                   18.780532                         NaN                             NaN                         NaN                           NaN                                  0.0                                     0.000000                               0.0                                  0.000000   STATE_OWNED                   125.0                           0.7              0.0                 1.0                 1.0           1.0            OK              COOPERATIVE
```

## Exact dataset

Scenarios: 4096; rows: 12288; solver failures: 0.

## Mode-specific value, investment, timing and transaction summaries

### JOINT_VENTURE

```text
        system_npv      value_C      value_U      value_T  expected_active_years  expected_total_quantity  expected_total_utilization  expected_total_storage  max_static_accounting_error  max_backward_forward_value_error  max_probability_mass_error  invest_prob_C  never_invest_prob_C  expected_tau_C_conditional  invest_prob_U  never_invest_prob_U  expected_tau_U_conditional  co2_trade_year_probability  storage_trade_year_probability  mean_co2_price_conditional  mean_storage_fee_conditional  mixed_equilibrium_state_probability  multiple_pure_equilibrium_state_probability  expected_mixed_equilibrium_years  expected_multiple_pure_equilibrium_years  transport_market_price  effective_abatement_fraction  storage_subsidy  capex_C_multiplier  capex_U_multiplier  carbon_scale  scenario_id
count  4096.000000  4096.000000  4096.000000  4096.000000            4096.000000              4096.000000                 4096.000000             4096.000000                 4.096000e+03                      4.096000e+03                4.096000e+03    4096.000000          4096.000000                 4096.000000    4096.000000          4096.000000                 4096.000000                 4096.000000                             0.0                 4096.000000                           0.0                               4096.0                                  4096.000000                            4096.0                               4096.000000             4096.000000                   4096.000000      4096.000000         4096.000000         4096.000000   4096.000000   4096.00000
mean    782.661510   283.137637   386.268818   113.255055              13.941403                 6.970701                    1.394140                5.576561                 1.222772e-12                      5.122223e-13                2.507218e-16       0.624212             0.375788                   10.092472       0.624212             0.375788                   10.092472                    0.464713                             NaN                  178.229650                           NaN                                  0.0                                     0.020807                               0.0                                  0.624212              137.500000                      0.750000        60.000000            1.000000            1.000000      3.375000   2047.50000
std     810.084861   308.177683   379.952162   123.271073               9.899678                 4.949839                    0.989968                3.959871                 7.523918e-13                      7.278652e-13                8.982740e-17       0.330695             0.330695                    6.687723       0.330695             0.330695                    6.687723                    0.329989                             NaN                   60.376869                           NaN                                  0.0                                     0.011023                               0.0                                  0.330695               36.088797                      0.144355        34.645246            0.173226            0.173226      1.660085   1182.55768
min       0.019518     0.002038     0.016665     0.000815               0.002554                 0.001277                    0.000255                0.001022                 1.136868e-13                      0.000000e+00                1.110223e-16       0.000472             0.000000                    0.000000       0.000472             0.000000                    0.000000                    0.000085                             NaN                  -47.081264                           NaN                                  0.0                                     0.000016                               0.0                                  0.000472               75.017189                      0.500003         0.006302            0.700116            0.700136      0.500223      0.00000
5%        3.637770     0.894569     2.369798     0.357828               0.288657                 0.144329                    0.028866                0.115463                 2.273737e-13                      1.332268e-15                1.110223e-16       0.034296             0.000000                    0.000000       0.034296             0.000000                    0.000000                    0.009622                             NaN                   62.845455                           NaN                                  0.0                                     0.001143                               0.0                                  0.034296               81.269524                      0.525061         6.014231            0.729999            0.730109      0.788187    204.75000
50%     513.845263   175.999794   265.976408    70.399918              13.441964                 6.720982                    1.344196                5.376786                 9.094947e-13                      2.273737e-13                2.220446e-16       0.714929             0.285071                   10.198177       0.714929             0.285071                   10.198177                    0.448065                             NaN                  185.853536                           NaN                                  0.0                                     0.023831                               0.0                                  0.714929              137.510245                      0.750016        60.009516            1.000040            1.000001      3.375335   2047.50000
95%    2475.633201   942.755928  1161.097434   377.102371              29.000000                14.500000                    2.900000               11.600000                 1.818989e-12                      2.046363e-12                4.440892e-16       1.000000             0.965704                   20.227509       1.000000             0.965704                   20.227509                    0.966667                             NaN                  261.629669                           NaN                                  0.0                                     0.033333                               0.0                                  1.000000              193.749386                      0.974907       113.988311            1.269922            1.269892      5.961929   3890.25000
max    3793.323071  1547.562562  1626.735484   619.025025              29.000000                14.500000                    2.900000               11.600000                 3.637979e-12                      5.911716e-12                4.440892e-16       1.000000             0.999528                   23.588066       1.000000             0.999528                   23.588066                    0.966667                             NaN                  306.478049                           NaN                                  0.0                                     0.033333                               0.0                                  1.000000              199.995610                      0.999968       119.974735            1.299951            1.299872      6.248823   4095.00000
```

Mean annual mixed Nash frequency: 0; pure Nash frequency: 1; multiple-pure frequency: 0.020807070715543226.

### STATE_OWNED

```text
        system_npv      value_C      value_U  value_T  expected_active_years  expected_total_quantity  expected_total_utilization  expected_total_storage  max_static_accounting_error  max_backward_forward_value_error  max_probability_mass_error  invest_prob_C  never_invest_prob_C  expected_tau_C_conditional  invest_prob_U  never_invest_prob_U  expected_tau_U_conditional  co2_trade_year_probability  storage_trade_year_probability  mean_co2_price_conditional  mean_storage_fee_conditional  mixed_equilibrium_state_probability  multiple_pure_equilibrium_state_probability  expected_mixed_equilibrium_years  expected_multiple_pure_equilibrium_years  transport_market_price  effective_abatement_fraction  storage_subsidy  capex_C_multiplier  capex_U_multiplier  carbon_scale  scenario_id
count  4096.000000  4096.000000  4096.000000      0.0            4096.000000              4096.000000                 4096.000000             4096.000000                 4.096000e+03                      4.096000e+03                4.096000e+03    4096.000000          4096.000000                 4096.000000    4096.000000          4096.000000                 4096.000000                         0.0                             0.0                         0.0                           0.0                               4096.0                                       4096.0                            4096.0                                    4096.0             4096.000000                   4096.000000      4096.000000         4096.000000         4096.000000   4096.000000   4096.00000
mean    800.319824   800.319824   800.319824      NaN              16.689658                 8.344829                    1.668966                6.675863                 2.397197e-13                      4.626929e-13                2.553025e-16       0.694106             0.305894                    8.081662       0.694106             0.305894                    8.081662                         NaN                             NaN                         NaN                           NaN                                  0.0                                          0.0                               0.0                                       0.0              137.500000                      0.750000        60.000000            1.000000            1.000000      3.375000   2047.50000
std     812.545436   812.545436   812.545436      NaN              10.430325                 5.215163                    1.043033                4.172130                 2.348960e-13                      7.255509e-13                9.087218e-17       0.326225             0.326225                    6.861424       0.326225             0.326225                    6.861424                         NaN                             NaN                         NaN                           NaN                                  0.0                                          0.0                               0.0                                       0.0               36.088797                      0.144355        34.645246            0.173226            0.173226      1.660085   1182.55768
min       0.024523     0.024523     0.024523      NaN               0.004741                 0.002371                    0.000474                0.001897                 2.842171e-14                      0.000000e+00                1.110223e-16       0.000734             0.000000                    0.000000       0.000734             0.000000                    0.000000                         NaN                             NaN                         NaN                           NaN                                  0.0                                          0.0                               0.0                                       0.0               75.017189                      0.500003         0.006302            0.700116            0.700136      0.500223      0.00000
5%        4.117809     4.117809     4.117809      NaN               0.470027                 0.235013                    0.047003                0.188011                 5.684342e-14                      0.000000e+00                1.110223e-16       0.051409             0.000000                    0.000000       0.051409             0.000000                    0.000000                         NaN                             NaN                         NaN                           NaN                                  0.0                                          0.0                               0.0                                       0.0               81.269524                      0.525061         6.014231            0.729999            0.730109      0.788187    204.75000
50%     538.025049   538.025049   538.025049      NaN              16.876273                 8.438136                    1.687627                6.750509                 1.136868e-13                      1.705303e-13                2.220446e-16       0.818184             0.181816                    7.931454       0.818184             0.181816                    7.931454                         NaN                             NaN                         NaN                           NaN                                  0.0                                          0.0                               0.0                                       0.0              137.510245                      0.750016        60.009516            1.000040            1.000001      3.375335   2047.50000
95%    2475.633201  2475.633201  2475.633201      NaN              29.000000                14.500000                    2.900000               11.600000                 9.094947e-13                      1.818989e-12                4.440892e-16       1.000000             0.948591                   19.566423       1.000000             0.948591                   19.566423                         NaN                             NaN                         NaN                           NaN                                  0.0                                          0.0                               0.0                                       0.0              193.749386                      0.974907       113.988311            1.269922            1.269892      5.961929   3890.25000
max    3793.323071  3793.323071  3793.323071      NaN              29.000000                14.500000                    2.900000               11.600000                 1.818989e-12                      5.911716e-12                4.440892e-16       1.000000             0.999266                   22.726804       1.000000             0.999266                   22.726804                         NaN                             NaN                         NaN                           NaN                                  0.0                                          0.0                               0.0                                       0.0              199.995610                      0.999968       119.974735            1.299951            1.299872      6.248823   4095.00000
```

Cooperative selection, not a Nash game; mixed and multiple-pure fields equal 0.0.

### TRANSFER

```text
        system_npv      value_C      value_U      value_T  expected_active_years  expected_total_quantity  expected_total_utilization  expected_total_storage  max_static_accounting_error  max_backward_forward_value_error  max_probability_mass_error  invest_prob_C  never_invest_prob_C  expected_tau_C_conditional  invest_prob_U  never_invest_prob_U  expected_tau_U_conditional  co2_trade_year_probability  storage_trade_year_probability  mean_co2_price_conditional  mean_storage_fee_conditional  mixed_equilibrium_state_probability  multiple_pure_equilibrium_state_probability  expected_mixed_equilibrium_years  expected_multiple_pure_equilibrium_years  transport_market_price  effective_abatement_fraction  storage_subsidy  capex_C_multiplier  capex_U_multiplier  carbon_scale  scenario_id
count  4096.000000  4096.000000  4096.000000  4096.000000            4096.000000              4096.000000                 4096.000000             4096.000000                 4.096000e+03                      4.096000e+03                4.096000e+03    4096.000000          4096.000000                 4096.000000    4096.000000          4096.000000                 4096.000000                 4096.000000                     4096.000000                 4096.000000                   4096.000000                               4096.0                                  4096.000000                            4096.0                               4096.000000             4096.000000                   4096.000000      4096.000000         4096.000000         4096.000000   4096.000000   4096.00000
mean    790.522784   286.277009   490.729174    13.516601              13.929037                 5.836387                    1.392904                4.443483                 1.307038e-12                      5.535211e-13                2.383618e-16       0.587158             0.412842                    9.153643       0.587158             0.412842                    9.153643                    0.464301                        0.370290                  175.378465                    216.003990                                  0.0                                     0.019572                               0.0                                  0.587158              137.500000                      0.750000        60.000000            1.000000            1.000000      3.375000   2047.50000
std     814.672177   321.668205   487.824582    88.699841              10.451311                 4.435618                    1.045131                3.412082                 7.324785e-13                      7.725760e-13                9.010851e-17       0.350924             0.350924                    6.598294       0.350924             0.350924                    6.598294                    0.348377                        0.284340                   60.408655                     58.184703                                  0.0                                     0.011697                               0.0                                  0.350924               36.088797                      0.144355        34.645246            0.173226            0.173226      1.660085   1182.55768
min       0.007769     0.000798     0.007267  -270.973206               0.000474                 0.000233                    0.000047                0.000186                 1.136868e-13                      3.469447e-18                1.110223e-16       0.000082             0.000000                    0.000000       0.000082             0.000000                    0.000000                    0.000016                        0.000015                  -55.058361                     87.934044                                  0.0                                     0.000003                               0.0                                  0.000082               75.017189                      0.500003         0.006302            0.700116            0.700136      0.500223      0.00000
5%        2.491388     0.491374     1.817356  -142.659803               0.120540                 0.056620                    0.012054                0.044566                 2.273737e-13                      8.881784e-16                1.110223e-16       0.012626             0.000000                    0.000000       0.012626             0.000000                    0.000000                    0.004018                        0.003714                   65.551504                    131.221798                                  0.0                                     0.000421                               0.0                                  0.012626               81.269524                      0.525061         6.014231            0.729999            0.730109      0.788187    204.75000
50%     520.665910   167.072637   333.087874     2.296984              12.709474                 5.382004                    1.270947                4.051857                 1.818989e-12                      2.273737e-13                2.220446e-16       0.649331             0.350669                    9.426803       0.649331             0.350669                    9.426803                    0.423649                        0.337655                  178.740046                    208.983248                                  0.0                                     0.021644                               0.0                                  0.649331              137.510245                      0.750016        60.009516            1.000040            1.000001      3.375335   2047.50000
95%    2478.591030   976.194220  1481.708142   182.142375              29.000000                13.178022                    2.900000               10.278022                 1.818989e-12                      2.046363e-12                4.440892e-16       1.000000             0.987374                   19.713731       1.000000             0.987374                   19.713731                    0.966667                        0.856502                  268.057597                    324.231666                                  0.0                                     0.033333                               0.0                                  1.000000              193.749386                      0.974907       113.988311            1.269922            1.269892      5.961929   3890.25000
max    3782.095843  1640.755813  2177.880457   373.383546              29.000000                14.061252                    2.900000               11.161252                 3.637979e-12                      7.730705e-12                4.440892e-16       1.000000             0.999918                   23.253572       1.000000             0.999918                   23.253572                    0.966667                        0.930104                  329.158979                    438.567157                                  0.0                                     0.033333                               0.0                                  1.000000              199.995610                      0.999968       119.974735            1.299951            1.299872      6.248823   4095.00000
```

Mean annual mixed Nash frequency: 0; pure Nash frequency: 1; multiple-pure frequency: 0.019571924565431376.

## Surrogate test metrics

```text
         mode                       target split   n       R2       MAE      RMSE     NMAE predictions gate_pass
     TRANSFER                   system_npv  test 614 0.996827 30.452447 47.045291 0.011827   UNCLIPPED      True
     TRANSFER                      value_C  test 614 0.996140 11.928252 20.688154 0.011544   UNCLIPPED      True
     TRANSFER                      value_T  test 614 0.989714  5.164945  8.971146 0.016307   UNCLIPPED      True
     TRANSFER                      value_U  test 614 0.994841 23.499470 36.182902 0.015422   UNCLIPPED      True
     TRANSFER                invest_prob_C  test 614 0.995566  0.016752  0.023655 0.016980   UNCLIPPED      True
     TRANSFER                invest_prob_U  test 614 0.995566  0.016752  0.023655 0.016980   UNCLIPPED      True
     TRANSFER   expected_tau_C_conditional  test 614 0.986688  0.565208  0.768975 0.028291   UNCLIPPED      True
     TRANSFER   expected_tau_U_conditional  test 614 0.986688  0.565208  0.768975 0.028291   UNCLIPPED      True
     TRANSFER   mean_co2_price_conditional  test 614 0.979397  6.934198  9.008790 0.033271   UNCLIPPED      True
     TRANSFER mean_storage_fee_conditional  test 614 0.974491  7.557412  9.538747 0.037058   UNCLIPPED      True
JOINT_VENTURE                   system_npv  test 614 0.997559 25.787106 41.246964 0.010008   UNCLIPPED      True
JOINT_VENTURE                      value_C  test 614 0.997091  9.884621 17.243438 0.009886   UNCLIPPED      True
JOINT_VENTURE                      value_T  test 614 0.997091  3.953849  6.897375 0.009886   UNCLIPPED      True
JOINT_VENTURE                      value_U  test 614 0.997167 13.701308 20.700445 0.011551   UNCLIPPED      True
JOINT_VENTURE                invest_prob_C  test 614 0.997323  0.013238  0.017449 0.013648   UNCLIPPED      True
JOINT_VENTURE                invest_prob_U  test 614 0.997323  0.013238  0.017449 0.013648   UNCLIPPED      True
JOINT_VENTURE   expected_tau_C_conditional  test 614 0.987473  0.592280  0.765222 0.028821   UNCLIPPED      True
JOINT_VENTURE   expected_tau_U_conditional  test 614 0.987473  0.592280  0.765222 0.028821   UNCLIPPED      True
JOINT_VENTURE   mean_co2_price_conditional  test 614 0.977314  7.362434  9.196366 0.037440   UNCLIPPED      True
  STATE_OWNED                   system_npv  test 614 0.997731 25.436596 39.877398 0.009874   UNCLIPPED      True
  STATE_OWNED                invest_prob_C  test 614 0.997063  0.013012  0.018053 0.013714   UNCLIPPED      True
  STATE_OWNED                invest_prob_U  test 614 0.997063  0.013012  0.018053 0.013714   UNCLIPPED      True
  STATE_OWNED   expected_tau_C_conditional  test 614 0.988959  0.533336  0.733911 0.027119   UNCLIPPED      True
  STATE_OWNED   expected_tau_U_conditional  test 614 0.988959  0.533336  0.733911 0.027119   UNCLIPPED      True
```

## Exact-verified boundaries (all roots and found=false rows)

```text
                    variable          mode    boundary_type          role  surrogate_false_brackets  found  boundary_value  bracket_lower  bracket_upper  response_lower  response_upper  closest_grid_value  closest_response
      transport_market_price      TRANSFER  SYSTEM_NPV_ZERO supplementary                         4  False             NaN            NaN            NaN             NaN             NaN          192.812500         -0.131206
      transport_market_price      TRANSFER C_INVEST_PROB_50 supplementary                         0  False             NaN            NaN            NaN             NaN             NaN          115.937500          0.041219
      transport_market_price      TRANSFER U_INVEST_PROB_50 supplementary                         0  False             NaN            NaN            NaN             NaN             NaN          115.937500          0.041219
      transport_market_price JOINT_VENTURE  SYSTEM_NPV_ZERO supplementary                         0  False             NaN            NaN            NaN             NaN             NaN          121.250000          2.382750
      transport_market_price JOINT_VENTURE C_INVEST_PROB_50 supplementary                         0  False             NaN            NaN            NaN             NaN             NaN          121.562500          0.049753
      transport_market_price JOINT_VENTURE U_INVEST_PROB_50 supplementary                         0  False             NaN            NaN            NaN             NaN             NaN          121.562500          0.049753
      transport_market_price   STATE_OWNED  SYSTEM_NPV_ZERO supplementary                         0  False             NaN            NaN            NaN             NaN             NaN          116.875000          8.710379
      transport_market_price   STATE_OWNED C_INVEST_PROB_50 supplementary                         0  False             NaN            NaN            NaN             NaN             NaN          104.687500          0.076542
      transport_market_price   STATE_OWNED U_INVEST_PROB_50 supplementary                         0  False             NaN            NaN            NaN             NaN             NaN          104.687500          0.076542
effective_abatement_fraction      TRANSFER  SYSTEM_NPV_ZERO supplementary                         3  False             NaN            NaN            NaN             NaN             NaN            0.526250         -0.173069
effective_abatement_fraction      TRANSFER C_INVEST_PROB_50 supplementary                         0  False             NaN            NaN            NaN             NaN             NaN            0.996250          0.097065
effective_abatement_fraction      TRANSFER U_INVEST_PROB_50 supplementary                         0  False             NaN            NaN            NaN             NaN             NaN            0.996250          0.097065
effective_abatement_fraction JOINT_VENTURE  SYSTEM_NPV_ZERO supplementary                         5  False             NaN            NaN            NaN             NaN             NaN            0.578750          0.046387
effective_abatement_fraction JOINT_VENTURE C_INVEST_PROB_50 supplementary                         0  False             NaN            NaN            NaN             NaN             NaN            0.991250          0.130261
effective_abatement_fraction JOINT_VENTURE U_INVEST_PROB_50 supplementary                         0  False             NaN            NaN            NaN             NaN             NaN            0.991250          0.130261
effective_abatement_fraction   STATE_OWNED  SYSTEM_NPV_ZERO supplementary                         1  False             NaN            NaN            NaN             NaN             NaN            0.553750          0.219757
effective_abatement_fraction   STATE_OWNED C_INVEST_PROB_50 supplementary                         0  False             NaN            NaN            NaN             NaN             NaN            0.992500          0.204257
effective_abatement_fraction   STATE_OWNED U_INVEST_PROB_50 supplementary                         0  False             NaN            NaN            NaN             NaN             NaN            0.992500          0.204257
             storage_subsidy      TRANSFER  SYSTEM_NPV_ZERO supplementary                         0  False             NaN            NaN            NaN             NaN             NaN          109.500000          7.622497
             storage_subsidy      TRANSFER C_INVEST_PROB_50 supplementary                         0  False             NaN            NaN            NaN             NaN             NaN           44.400000          0.045681
             storage_subsidy      TRANSFER U_INVEST_PROB_50 supplementary                         0  False             NaN            NaN            NaN             NaN             NaN           44.400000          0.045681
             storage_subsidy JOINT_VENTURE  SYSTEM_NPV_ZERO supplementary                         0  False             NaN            NaN            NaN             NaN             NaN            0.000000          5.483010
             storage_subsidy JOINT_VENTURE C_INVEST_PROB_50 supplementary                         0  False             NaN            NaN            NaN             NaN             NaN          119.100000          0.088600
             storage_subsidy JOINT_VENTURE U_INVEST_PROB_50 supplementary                         0  False             NaN            NaN            NaN             NaN             NaN          119.100000          0.088600
             storage_subsidy   STATE_OWNED  SYSTEM_NPV_ZERO supplementary                         0  False             NaN            NaN            NaN             NaN             NaN            3.000000          9.626435
             storage_subsidy   STATE_OWNED C_INVEST_PROB_50 supplementary                         0  False             NaN            NaN            NaN             NaN             NaN          113.700000          0.137236
             storage_subsidy   STATE_OWNED U_INVEST_PROB_50 supplementary                         0  False             NaN            NaN            NaN             NaN             NaN          113.700000          0.137236
          capex_C_multiplier      TRANSFER  SYSTEM_NPV_ZERO supplementary                         4  False             NaN            NaN            NaN             NaN             NaN            1.124500          0.175981
          capex_C_multiplier      TRANSFER C_INVEST_PROB_50 supplementary                         0  False             NaN            NaN            NaN             NaN             NaN            0.709000          0.088620
          capex_C_multiplier      TRANSFER U_INVEST_PROB_50 supplementary                         0  False             NaN            NaN            NaN             NaN             NaN            0.709000          0.088620
          capex_C_multiplier JOINT_VENTURE  SYSTEM_NPV_ZERO supplementary                         7  False             NaN            NaN            NaN             NaN             NaN            1.201000          0.058970
          capex_C_multiplier JOINT_VENTURE C_INVEST_PROB_50 supplementary                         0  False             NaN            NaN            NaN             NaN             NaN            0.700000          0.075723
          capex_C_multiplier JOINT_VENTURE U_INVEST_PROB_50 supplementary                         0  False             NaN            NaN            NaN             NaN             NaN            0.700000          0.075723
          capex_C_multiplier   STATE_OWNED  SYSTEM_NPV_ZERO supplementary                         0  False             NaN            NaN            NaN             NaN             NaN            1.156000          5.000443
          capex_C_multiplier   STATE_OWNED C_INVEST_PROB_50 supplementary                         0  False             NaN            NaN            NaN             NaN             NaN            0.736000          0.107652
          capex_C_multiplier   STATE_OWNED U_INVEST_PROB_50 supplementary                         0  False             NaN            NaN            NaN             NaN             NaN            0.736000          0.107652
          capex_U_multiplier      TRANSFER  SYSTEM_NPV_ZERO supplementary                         0  False             NaN            NaN            NaN             NaN             NaN            1.253500          2.294874
          capex_U_multiplier      TRANSFER C_INVEST_PROB_50 supplementary                         0  False             NaN            NaN            NaN             NaN             NaN            1.270000          0.041732
          capex_U_multiplier      TRANSFER U_INVEST_PROB_50 supplementary                         0  False             NaN            NaN            NaN             NaN             NaN            1.270000          0.041732
          capex_U_multiplier JOINT_VENTURE  SYSTEM_NPV_ZERO supplementary                         0  False             NaN            NaN            NaN             NaN             NaN            1.175500          1.249490
          capex_U_multiplier JOINT_VENTURE C_INVEST_PROB_50 supplementary                         0  False             NaN            NaN            NaN             NaN             NaN            0.700000          0.056035
          capex_U_multiplier JOINT_VENTURE U_INVEST_PROB_50 supplementary                         0  False             NaN            NaN            NaN             NaN             NaN            0.700000          0.056035
          capex_U_multiplier   STATE_OWNED  SYSTEM_NPV_ZERO supplementary                         0  False             NaN            NaN            NaN             NaN             NaN            1.277500          6.745210
          capex_U_multiplier   STATE_OWNED C_INVEST_PROB_50 supplementary                         0  False             NaN            NaN            NaN             NaN             NaN            0.700000          0.084073
          capex_U_multiplier   STATE_OWNED U_INVEST_PROB_50 supplementary                         0  False             NaN            NaN            NaN             NaN             NaN            0.700000          0.084073
                carbon_scale      TRANSFER  SYSTEM_NPV_ZERO          main                         0  False             NaN            NaN            NaN             NaN             NaN            0.672500          2.103097
                carbon_scale      TRANSFER     C_VALUE_ZERO          main                         1  False             NaN            NaN            NaN             NaN             NaN            0.571875          0.000815
                carbon_scale      TRANSFER     U_VALUE_ZERO          main                         1  False             NaN            NaN            NaN             NaN             NaN            0.888125          0.251370
                carbon_scale      TRANSFER C_INVEST_PROB_50          main                         1  False             NaN            NaN            NaN             NaN             NaN            2.958125          0.510375
                carbon_scale      TRANSFER U_INVEST_PROB_50          main                         1  False             NaN            NaN            NaN             NaN             NaN            2.958125          0.510375
                carbon_scale      TRANSFER   CO2_PRICE_ZERO          main                         0  False             NaN            NaN            NaN             NaN             NaN            6.192500        111.464425
                carbon_scale      TRANSFER STORAGE_FEE_ZERO          main                         0  False             NaN            NaN            NaN             NaN             NaN            0.730000        184.596703
                carbon_scale JOINT_VENTURE  SYSTEM_NPV_ZERO          main                         1  False             NaN            NaN            NaN             NaN             NaN            0.787500          0.387886
                carbon_scale JOINT_VENTURE     C_VALUE_ZERO          main                         0  False             NaN            NaN            NaN             NaN             NaN            0.500000          0.096114
                carbon_scale JOINT_VENTURE     U_VALUE_ZERO          main                         0  False             NaN            NaN            NaN             NaN             NaN            0.500000          0.563462
                carbon_scale JOINT_VENTURE C_INVEST_PROB_50          main                         1  False             NaN            NaN            NaN             NaN             NaN            2.843125          0.502363
                carbon_scale JOINT_VENTURE U_INVEST_PROB_50          main                         1  False             NaN            NaN            NaN             NaN             NaN            2.843125          0.502363
                carbon_scale JOINT_VENTURE   CO2_PRICE_ZERO          main                         0  False             NaN            NaN            NaN             NaN             NaN            6.192500         88.193290
                carbon_scale   STATE_OWNED  SYSTEM_NPV_ZERO          main                         0  False             NaN            NaN            NaN             NaN             NaN            0.500000          2.251371
                carbon_scale   STATE_OWNED C_INVEST_PROB_50          main                         1  False             NaN            NaN            NaN             NaN             NaN            2.440625          0.504881
                carbon_scale   STATE_OWNED U_INVEST_PROB_50          main                         1  False             NaN            NaN            NaN             NaN             NaN            2.440625          0.504881
```

Surrogate false brackets and exact evaluations are in boundaries/verification. Crossing intervals may bracket jumps; a midpoint is not asserted to be an exact response-equality point.

Searches: 61; found=false rows: 61; discarded surrogate false brackets: 33.

Interpretation limit: found=false means the prescribed surrogate-candidate/exact-verification procedure retained no crossing. It does not prove absence of a crossing throughout the full economic domain. Candidates without an exact endpoint crossing are discarded, not widened. No alternative search algorithm was introduced. closest_response is from the surrogate grid, as labeled in each verification record.

## Structural NaN

Conditional investment times are NaN when investment probability <1e-12. Conditional prices are NaN when transaction-year denominator <1e-12. JV storage and both SOE internal transaction mechanisms are structurally inapplicable. SOE value_T is not an individual economic result and is NaN; SOE value_C=value_U=system value for cooperative decisions.

## RL benchmark and provenance

# RL benchmark note

以下历史信息由主规范第 53、82 节提供；当前工作区没有旧项目及其正式产物，
尚不能通过 checkpoint、formal_run_lock 或 Gate 报告独立核验：

- 旧 AS-CTDE-PPO 已完成 15 个正式 policy。
- Gate 4 完整性通过，原 Critic accuracy Gate 未通过。
- 初始研究探索并完成正式策略训练与经济核验，但价值近似精度未达到预设标准。
- 因此本轮主框架采用可解释的有限期随机动态投资博弈，再训练代理用于参数映射和边界识别。

这些信息不构成对 RL 方法无效的判断。旧结果未混入精确求解数据集，
未修改旧 checkpoint、formal_run_lock 或 Gate 4/5 正式结果。


Old RL project modified: NO. Old RL formal results overwritten: NO.

## Pytest Temporary Directory Incident

- 原始错误：Windows default temp PermissionError / WinError 5。
- 原错误发生于两个恢复测试的 tmp_path fixture setup；尚未进入测试断言。
- 在受限执行环境中，项目内目录的第一次最小写入检查也失败；用户随后解除文件系统限制并授权重试。
- 重试 .pytest_tmp 最小写入检查：输出 ok，exit code=0。
- 解决方式：project-local --basetemp=.pytest_tmp；pytest.ini 设置 addopts=-p no:cacheprovider --basetemp=.pytest_tmp，.gitignore 忽略 .pytest_tmp/ 和 .pytest_cache/。
- 分类：TEST_INFRASTRUCTURE_ONLY。未修改 Windows ACL，未启动管理员会话，未修改测试断言、研究参数或 Gate，未 skip/xfail 测试。
- 修复后完整命令：D:/anaconda3/python.exe -m pytest -q -p no:cacheprovider --basetemp=.pytest_tmp。
- 完整结果：52 passed in 2.04s，failed=0、errors=0、skipped=0、exit code=0。
- compileall：D:/anaconda3/python.exe -m compileall -q .，exit code=0。
- 项目未提供 .venv/Scripts/python.exe，因此继续使用原先已记录的 Python 3.13.9 环境 D:/anaconda3/python.exe，没有切换依赖版本。
- config SHA256：3b928b7fa65ee90acf52fe1c968de855cddddf3c81b5a2661d9ffd134bd48e76。
- source_manifest_hash：2d53befd84c4ab357af40aa9c96a6f17ee6c959eb32c4af79196a68d8946eef0。
- 23 个源码文件、12 个测试文件逐一匹配上次中断 manifest，无研究源码或测试变更。
- Git SHA / worktree status：当前目录不是 Git 仓库，命令返回 128，不虚构 Git commit。
- 先前失败记录仍保留供审计；不能将历史失败记录误作本次修复后的测试结果。

## Gates

Gates 1–7 PASS; final compile/tests PASS. FINAL STATUS: ALL_STAGES_COMPLETED.
