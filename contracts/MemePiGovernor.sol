// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

interface IMemePiStaking {
    function stakeOf(address account) external view returns (uint256);
}

contract MemePiGovernor {
    address public owner;
    IMemePiStaking public staking;
    uint256 public proposalCount;
    uint256 public votingPeriod; // seconds
    uint256 public quorum; // minimum total votes (in wei amount of MEPI) required

    struct Proposal {
        address proposer;
        string description;
        uint256 startTime;
        uint256 forVotes;
        uint256 againstVotes;
        uint256 abstainVotes;
        bool executed;
        mapping(address => bool) hasVoted;
    }

    mapping(uint256 => Proposal) private proposals;

    event ProposalCreated(uint256 id, address proposer, string description, uint256 startTime);
    event Voted(uint256 id, address voter, uint8 support, uint256 weight);
    event ProposalExecuted(uint256 id, bool passed);

    modifier onlyOwner() {
        require(msg.sender == owner, "only owner");
        _;
    }

    constructor(address _staking, uint256 _votingPeriodSeconds, uint256 _quorum) {
        owner = msg.sender;
        staking = IMemePiStaking(_staking);
        votingPeriod = _votingPeriodSeconds;
        quorum = _quorum;
    }

    function createProposal(string calldata description) external returns (uint256) {
        proposalCount++;
        uint256 id = proposalCount;
        Proposal storage p = proposals[id];
        p.proposer = msg.sender;
        p.description = description;
        p.startTime = block.timestamp;
        emit ProposalCreated(id, msg.sender, description, p.startTime);
        return id;
    }

    // support: 0 = against, 1 = for, 2 = abstain
    function vote(uint256 proposalId, uint8 support) external {
        require(proposalId > 0 && proposalId <= proposalCount, "invalid id");
        Proposal storage p = proposals[proposalId];
        require(block.timestamp <= p.startTime + votingPeriod, "voting closed");
        require(!p.hasVoted[msg.sender], "already voted");
        uint256 weight = staking.stakeOf(msg.sender);
        require(weight > 0, "no voting power");
        p.hasVoted[msg.sender] = true;
        if (support == 0) {
            p.againstVotes += weight;
        } else if (support == 1) {
            p.forVotes += weight;
        } else {
            p.abstainVotes += weight;
        }
        emit Voted(proposalId, msg.sender, support, weight);
    }

    // check proposal status
    function proposalResult(uint256 id) public view returns (bool passed, uint256 forVotes, uint256 againstVotes, uint256 abstainVotes) {
        Proposal storage p = proposals[id];
        passed = (p.forVotes + p.againstVotes + p.abstainVotes) >= quorum && p.forVotes > p.againstVotes;
        return (passed, p.forVotes, p.againstVotes, p.abstainVotes);
    }

    // execute: for now, execution is just a flag flip; in production this should call a timelock or allowed actions
    function executeProposal(uint256 id) external onlyOwner {
        require(id > 0 && id <= proposalCount, "invalid id");
        Proposal storage p = proposals[id];
        require(block.timestamp > p.startTime + votingPeriod, "voting not finished");
        require(!p.executed, "already executed");
        (bool passed,,,) = proposalResult(id);
        p.executed = true;
        emit ProposalExecuted(id, passed);
        // NOTE: real execution (moving funds, changing settings) should be implemented with care and timelock
    }

    // Admin setters
    function setVotingPeriod(uint256 seconds_) external onlyOwner {
        votingPeriod = seconds_;
    }
    function setQuorum(uint256 q) external onlyOwner {
        quorum = q;
    }
}
